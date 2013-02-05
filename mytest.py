from usps.api import USPS_CONNECTION_TEST_SECURE, USPS_CONNECTION
from usps.api.addressinformation import AddressValidate, ZipCodeLookup, CityStateLookup
from usps.api.ratecalculator import DomesticRateCalculator, InternationalRateCalculator
from usps.api.servicestandards import PriorityMailServiceStandards, PackageServicesServiceStandards, ExpressMailServiceCommitment, get_service_standards
from usps.api.tracking import TrackConfirm
from pprint import pprint
import json

# Your Username is 621OLYMP1079
# Your Password is 228QM69IV159

USERID = "621OLYMP1079"
PASSWORD = "228QM69IV159"

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
                                'Service': 'Express',
                                'ZipOrigination': '44106',
                                'ZipDestination': '97217',
                                'Pounds': '1',
                                'Ounces': '8',
#                                'Container': 'RECTANGULAR',
                                'Size': 'REGULAR',
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

print "Here is the response! %s" % response
for item in response:
    print 'Item: %s' % item
    
    
print json.dumps(response, indent=4)


