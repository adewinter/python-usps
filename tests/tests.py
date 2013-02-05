"""
Tests for USPS API wrappers
"""
import unittest
from usps.api import USPS_CONNECTION_TEST, USPS_CONNECTION
from usps.api.addressinformation import AddressValidate, ZipCodeLookup, CityStateLookup
from usps.api.ratecalculator import DomesticRateCalculator, InternationalRateCalculator
from usps.api.servicestandards import PriorityMailServiceStandards, PackageServicesServiceStandards, ExpressMailServiceCommitment, get_service_standards
from usps.api.tracking import TrackConfirm


USERID = None
PASSWORD = None

class TestRateCalculatorAPI(unittest.TestCase):
    """
    Tests for Rate Calculator API wrappers
    """
    def test_domestic_rate(self):
        """
        Ensure that Domestic Rate Calculator returns quotes in the expected format
        """
        connector = DomesticRateCalculator(USPS_CONNECTION, USERID, PASSWORD)
        response = connector.execute([{'Service': 'First Class',
                                       'FirstClassMailType': 'LETTER',
                                       'ZipOrigination': '44106',
                                       'ZipDestination': '97217',
                                       'Pounds': '0',
                                       'Ounces': '3.5',
                                       'Size': 'REGULAR',
                                       'Machinable': 'true'
                                       }, 
                                       {
                                        'Service': 'Priority',
                                        'ZipOrigination': '44106',
                                        'ZipDestination': '97217',
                                        'Pounds': '1',
                                        'Ounces': '8',
                                        'Container': 'NONRECTANGULAR',
                                        'Size': 'LARGE',
                                        'Width': '15',
                                        'Length': '30',
                                        'Height': '15',
                                        'Girth': '55'
                                        },
                                        {'Service': 'ALL',
                                         'FirstClassMailType': 'LETTER',
                                         'ZipOrigination': '90210',
                                         'ZipDestination': '97217',
                                         'Pounds': '8',
                                         'Ounces': '32',
                                         'Container': None,
                                         'Size': 'REGULAR',
                                         'Machinable': 'true'
                                        },
                                        ])
       
        for rate in [response[0], response[1]]:
            self.assertTrue('Postage' in rate)
            self.assertTrue('Rate' in rate['Postage'])
            
        self.assertTrue('Postage' in response[2])
        for postage in response[2]['Postage']:
            self.assertTrue('Rate' in postage)
            self.assertTrue('MailService' in postage)
        
        
        
    def test_international_rate(self):
        """
        Ensure that International Rate Calculator returns quotes in the expected format
        """
        connector = InternationalRateCalculator(USPS_CONNECTION, USERID, PASSWORD)
        response = connector.execute([{'Pounds': '3',
                                       'Ounces': '3',
                                       'Machinable': 'false',
                                       'MailType': 'Envelope',
                                       'Country': 'Canada',
                                       },
                                       {'Pounds': '4',
                                        'Ounces': '3',
                                        'MailType': 'Package',
                                        'GXG': {
                                                'Length': '46',
                                                'Width': '14',
                                                'Height': '15',
                                                'POBoxFlag': 'N',
                                                'GiftFlag': 'N'
                                                },
                                        'ValueOfContents': '250',
                                        'Country': 'Japan'
                                        }])
      
        for rate in response:
            self.assertTrue('Prohibitions' in rate)
            self.assertTrue('Restrictions' in rate)
            self.assertTrue('Observations' in rate)
            self.assertTrue('CustomsForms' in rate)
            self.assertTrue('ExpressMail' in rate)
            self.assertTrue('AreasServed' in rate)
            self.assertTrue('Service' in rate)
        
            for service in rate['Service']:
                self.assertTrue('Postage' in service)
                self.assertTrue('SvcCommitments' in service)
                self.assertTrue('SvcDescription' in service)
    
class TestServiceStandardsAPI(unittest.TestCase):
    """
    Tests for service standards API wrappers
    """
    def test_priority_service_standards(self):
        connector = PriorityMailServiceStandards(USPS_CONNECTION_TEST, USERID, PASSWORD)
        response = connector.execute([{'OriginZip': '4',
                                       'DestinationZip': '4'
                                    }])[0]


        self.assertEqual(response['OriginZip'], '4')
        self.assertEqual(response['DestinationZip'], '4')
        self.assertEqual(response['Days'], '1')
        
        response = connector.execute([{'OriginZip': '4',
                                       'DestinationZip': '5'
                                    }])[0]
                                                
        self.assertEqual(response['OriginZip'], '4')
        self.assertEqual(response['DestinationZip'], '5')
        self.assertEqual(response['Days'], '2')
        
    def test_package_service_standards(self):
        connector = PackageServicesServiceStandards(USPS_CONNECTION_TEST, USERID, PASSWORD)
        response = connector.execute([{'OriginZip': '4',
                                       'DestinationZip': '4'
                                    }])[0]
                                                
        self.assertEqual(response['OriginZip'], '4')
        self.assertEqual(response['DestinationZip'], '4')
        self.assertEqual(response['Days'], '2')
        
        response = connector.execute([{'OriginZip': '4',
                                       'DestinationZip': '600'
                                    }])[0]
                                                
        self.assertEqual(response['OriginZip'], '4')
        self.assertEqual(response['DestinationZip'], '600')
        self.assertEqual(response['Days'], '3')
        
    def test_express_service_commitment(self):
        connector = ExpressMailServiceCommitment(USPS_CONNECTION_TEST, USERID, PASSWORD)
        response = connector.execute([{
                                        'OriginZIP': '20770',
                                        'DestinationZIP': '11210',
                                        'Date': '05-Aug-2004'
                                    }])[0]
                                    
        
        self.assertEqual(response, {'Commitment': [
                                                   {'CommitmentName': 'Next Day',
                                                    'CommitmentSequence': 'A0115',
                                                    'CommitmentTime': '3:00 PM',
                                                    'Location': [
                                                                 {'City': 'GREENBELT',
                                                                  'CutOff': '6:00 PM',
                                                                  'Facility': 'EXPRESS MAIL COLLECTION BOX',
                                                                  'State': 'MD',
                                                                  'Street': '119 CENTER WAY',
                                                                  'Zip': '20770'},
                                                                  {'City': 'GREENBELT',
                                                                   'CutOff': '3:00 PM',
                                                                   'Facility': 'EXPRESS MAIL COLLECTION BOX',
                                                                   'State': 'MD',
                                                                   'Street': '7500 GREENWAY CENTER DRIVE',
                                                                   'Zip': '20770'}]},
                                                    {'CommitmentName': 'Next Day',
                                                     'CommitmentSequence': 'A0112',
                                                     'CommitmentTime': '12:00 PM',
                                                     'Location': [
                                                                  {'City': 'GREENBELT',
                                                                   'CutOff': '6:00 PM',
                                                                   'Facility': 'EXPRESS MAIL COLLECTION BOX',
                                                                   'State': 'MD',
                                                                   'Street': '119 CENTER WAY',
                                                                   'Zip': '20770'},
                                                                   {'City': 'GREENBELT',
                                                                    'CutOff': '3:00 PM',
                                                                    'Facility': 'EXPRESS MAIL COLLECTION BOX',
                                                                    'State': 'MD',
                                                                    'Street': '7500 GREENWAY CENTER DRIVE',
                                                                    'Zip': '20770'},
                                                                    {'City': 'BALTIMORE',
                                                                     'CutOff': '9:45 PM',
                                                                     'Facility': 'AIR MAIL FACILITY',
                                                                     'State': 'MD',
                                                                     'Street': 'ROUTE 170 BLDG C DOOR 19',
                                                                     'Zip': '21240'}
                                                                    ]
                                                     }],
                                    'Date': '05-Aug-2004',
                                    'DestinationCity': 'BROOKLYN',
                                    'DestinationState': 'NY',
                                    'DestinationZIP': '11210',
                                    'OriginCity': 'GREENBELT',
                                    'OriginState': 'MD',
                                    'OriginZIP': '20770',
                                    'Time': '11:30 AM'})

        
        response = connector.execute([{'OriginZIP': '207',
                                       'DestinationZIP': '11210',
                                       'Date': '',
                                    }])[0]
        
        self.assertEqual(response, {'DestinationCity': 'BROOKLYN', 
                                    'OriginState': 'MD', 
                                    'DestinationState': 'NY', 
                                    'OriginZIP': '207', 
                                    'DestinationZIP': '11210', 
                                    'Commitment': {'CommitmentTime': '3:00 PM', 
                                                   'CommitmentName': 'Next Day', 
                                                   'CommitmentSequence': 'A0115', 
                                                   'Location': [{'City': 'GREENBELT', 
                                                                 'Zip': '20770', 
                                                                 'CutOff': '6:00 PM', 
                                                                 'Facility': 'EXPRESS MAIL COLLECTION BOX', 
                                                                 'State': 'MD', 
                                                                 'Street': '119 CENTER WAY'}, 
                                                                 {'City': 'GREENBELT', 
                                                                  'Zip': '20770', 
                                                                  'CutOff': '3:00 PM', 
                                                                  'Facility': 'EXPRESS MAIL COLLECTION BOX', 
                                                                  'State': 'MD', 
                                                                  'Street': '7500 GREENWAY CENTER DRIVE'}]}, 
                                    'Time': '11:30 AM', 
                                    'Date': '05-Aug-2004', 
                                    'OriginCity': 'GREENBELT'})
        
    def test_get_service_standards(self):
        """
        Test the get_service_standards function
        """
        data = {'OriginZip':'207', 'DestinationZip':'11210', 'CLASSID': 27}
        delivery_time = get_service_standards(data, USPS_CONNECTION_TEST, USERID, PASSWORD)
        self.assertEqual(delivery_time, 'Next Day')
        
        data = {'OriginZip':'4', 'DestinationZip':'4', 'CLASSID': 0}
        delivery_time = get_service_standards(data, USPS_CONNECTION_TEST, USERID, PASSWORD)
        self.assertEqual(delivery_time, '2 Days')
        
        data = {'OriginZip':'97222', 'DestinationZip':'90210', 'CLASSID': 99}
        delivery_time = get_service_standards(data, USPS_CONNECTION_TEST, USERID, PASSWORD)
        self.assertEqual(delivery_time, False)


class TestTrackConfirmAPI(unittest.TestCase):
    """
    Tests for Track/Confirm API wrapper
    """
    def test_tracking(self):
        """
        Test Track/Confirm API connector
        """
        connector = TrackConfirm(USPS_CONNECTION_TEST, USERID, PASSWORD)
        response = connector.execute([{'ID':'EJ958083578US'},])[0]
        
        self.assertEqual(response['TrackSummary'], 'Your item was delivered at 8:10 am on June 1 in Wilmington DE 19801.')
        self.assertEqual(response['TrackDetail'][0], 'May 30 11:07 am NOTICE LEFT WILMINGTON DE 19801.')
        self.assertEqual(response['TrackDetail'][1], 'May 30 10:08 am ARRIVAL AT UNIT WILMINGTON DE 19850.')
        self.assertEqual(response['TrackDetail'][2], 'May 29 9:55 am ACCEPT OR PICKUP EDGEWATER NJ 07020.')

        response = connector.execute([{'ID': 'EJ958088694US'}])[0]
        self.assertEqual(response['TrackSummary'], 'Your item was delivered at 1:39 pm on June 1 in WOBURN MA 01815.')
        self.assertEqual(response['TrackDetail'][0], 'May 30 7:44 am NOTICE LEFT WOBURN MA 01815.')
        self.assertEqual(response['TrackDetail'][1], 'May 30 7:36 am ARRIVAL AT UNIT NORTH READING MA 01889.')
        self.assertEqual(response['TrackDetail'][2], 'May 29 6:00 pm ACCEPT OR PICKUP PORTSMOUTH NH 03801.')
        

class TestAddressInformationAPI(unittest.TestCase):
    """
    Tests for address lookup and validation services
    """
    def test_address_validate(self):
        connector = AddressValidate(USPS_CONNECTION_TEST, USERID, PASSWORD)
        response = connector.execute([{'Firmname': '',
                                       'Address1': '',
                                       'Address2':'6406 Ivy Lane',
                                       'City':'Greenbelt',
                                       'State':'MD',
                                       'Zip5': '',
                                       'Zip4': ''}])[0]
                                       
        self.assertEqual(response['Address2'], '6406 IVY LN')
        self.assertEqual(response['City'], 'GREENBELT')
        self.assertEqual(response['State'], 'MD')
        self.assertEqual(response['Zip5'], '20770')
        self.assertEqual(response['Zip4'], '1440')
        
        response = connector.execute([{'Firmname': '',
                                       'Address1': '',
                                       'Address2':'8 Wildwood Drive',
                                       'City':'Old Lyme',
                                       'State':'CT',
                                       'Zip5':'06371',
                                       'Zip4': ''}])[0]
                                       
        self.assertEqual(response['Address2'], '8 WILDWOOD DR')
        self.assertEqual(response['City'], 'OLD LYME')
        self.assertEqual(response['State'], 'CT')
        self.assertEqual(response['Zip5'], '06371')
        self.assertEqual(response['Zip4'], '1844')
    
    def test_zip_code_lookup(self):
        connector = ZipCodeLookup(USPS_CONNECTION_TEST, USERID, PASSWORD)
        response = connector.execute([{'Firmname': '',
                                       'Address1': '',
                                       'Address2':'6406 Ivy Lane',
                                       'City':'Greenbelt',
                                       'State':'MD'}])[0]
                                       
        self.assertEqual(response['Address2'], '6406 IVY LN')
        self.assertEqual(response['City'], 'GREENBELT')
        self.assertEqual(response['State'], 'MD')
        self.assertEqual(response['Zip5'], '20770')
        self.assertEqual(response['Zip4'], '1440')
        
        response = connector.execute([{'Firmname': '',
                                       'Address1': '',
                                       'Address2':'8 Wildwood Drive',
                                       'City':'Old Lyme',
                                       'State':'CT',
                                       'Zip5':'06371',}])[0]
                                       
        self.assertEqual(response['Address2'], '8 WILDWOOD DR')
        self.assertEqual(response['City'], 'OLD LYME')
        self.assertEqual(response['State'], 'CT')
        self.assertEqual(response['Zip5'], '06371')
        self.assertEqual(response['Zip4'], '1844')
    
    def test_city_state_lookup(self):
        connector = CityStateLookup(USPS_CONNECTION_TEST, USERID, PASSWORD)
        response = connector.execute([{'Zip5':'90210'}])[0]
        
        self.assertEqual(response['City'], 'BEVERLY HILLS')
        self.assertEqual(response['State'], 'CA')
        self.assertEqual(response['Zip5'], '90210')
        
        response = connector.execute([{'Zip5':'20770',}])[0]
        self.assertEqual(response['City'], 'GREENBELT')
        self.assertEqual(response['State'], 'MD')
        self.assertEqual(response['Zip5'], '20770')

if __name__ == '__main__':
    #please append your USPS USERID to test against the wire
    import sys
    if len(sys.argv) < 2:
        print "You must provide a USERID and PASSWORD"
        exit()
    else:
        USERID = sys.argv.pop()
        PASSWORD = sys.argv.pop()
        unittest.main()
