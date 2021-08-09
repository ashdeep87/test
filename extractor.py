import logging
import json
from types import SimpleNamespace
from collections import namedtuple

from typing import Any, Dict, List, Union
import phonenumbers

from client import (
    DataProvider,
)

from dtos import (
    Address,
    EducationElement,
    IndividualEducation,
    EmailAddress,
    EmploymentElement,
    IndividualEmployment,
    Phone,
    Name,
    URL,
    Individual,
    URLScheme
)

class DataExtractor:
    def __init__(self, data_client: DataProvider, logger=logging.Logger):
        self.data_client = data_client
        self.logger = logger
        self.names_list = []
        self.email_address_list = []
        self.address_list = []
        self.employment_list = []
        self.usernames_list = []
    
    def get_individual(self) -> Individual:
        file1Data = self.data_client.get_jsonFromFile('data1.txt')
        file2Data = self.data_client.get_jsonFromFile('data2.txt')

        merged_data = {**file1Data, **file2Data}
        structured_data = self._get_individual_dto(merged_data)
        return structured_data

    def _get_individual_dto(self, obj: Dict) -> Individual: 
        indiVidualInfo = obj["data"]["people"]["individualInfoBeta"]
        item_dto = Individual(
            gc_id=1234,
            semantic_gc_id= "",
            possible_names = self._get_possible_names(indiVidualInfo, obj),
            primary_name = self._get_name_dto1(indiVidualInfo),
            popular_aliases= [],
            addresses= self._get_addresses(indiVidualInfo, obj),
            email_addresses= self._get_email_addresses(indiVidualInfo, obj),
            tags=[],
            phones = self._get_phone_numbers(indiVidualInfo),
            urls= self._get_profile_Urls(indiVidualInfo),
            education= self._get_education_data(indiVidualInfo),
            employment= self._get_employement_data(indiVidualInfo, obj),
            usernames = self._get_usernames_list(indiVidualInfo)
        )

        return item_dto
    




    def _get_possible_names(self, obj1: Dict, obj2: Dict) -> None:  
        self.names_list.append(self._get_name_dto1(obj1))
        self.names_list.append(self._get_name_dto2(obj2))

        return self.names_list

    
    def _get_name_dto1(self, item: Dict) -> None:
        item_dto = Name(
            first_name = item.get('first_name'),
            last_name = item.get('last_name'),
            middle_names = [],
            prefix = None,
            suffix = None,
            full_name = item.get('first_name') + " " + item.get('last_name'),
            full_name_raw = item.get('full_name'),
        )
        return item_dto

    def _get_name_dto2(self, item: Dict) -> None:
        item_dto = Name(
            first_name = item.get('firstName'),
            last_name = item.get('lastName'),
            middle_names = [],
            prefix = None,
            suffix = None,
            full_name = item.get('firstName') + " "+item.get('lastName'),
            full_name_raw = item.get('fullName'),
        )
        return item_dto    





    def _get_addresses(self, obj1: Dict, obj2: Dict) -> None: 
        self.address_list.append(self._get_address_dto1(obj1))
        self.address_list.append(self._get_address_dto2(obj2))
        return self.address_list
        

    def _get_address_dto1(self, item: Dict) -> None:
        location = [x.strip() for x in item.get('location_name').split(',')]
        locationGeo = [x.strip() for x in item.get('location_geo').split(',')]
        item_dto = Address(
            city= location[0],
            country= location[2],
            state= location[1],
            latitude= locationGeo[0],
            longitude= locationGeo[1],
        )
        return item_dto    

    def _get_address_dto2(self, item: Dict) -> None:
        item_dto = Address(
            city= item.get('city'),
            country= item.get('country'),
            state= item.get('state'),
            latitude= None,
            longitude= None
        )
        return item_dto    




    def _get_email_addresses(self, obj1: Dict,  obj2: Dict) -> None: 
        self.email_address_list = [self._get_email_address_dto1(item) for item in obj1.get('emails')]
        self.email_address_list.append(self._get_email_address_dto2(obj2))
        return self.email_address_list

    def _get_email_address_dto1(self, item: Dict) -> None:
        item_dto = EmailAddress(
            email_address= item.get('address')
        )
        return item_dto    

    def _get_email_address_dto2(self, item: Dict) -> None:
        item_dto = EmailAddress(
            email_address= item.get('email')
        )
        return item_dto    





    def _get_phone_numbers(self, obj: Dict) -> None: 
        item_list = [self._get_phone_number_dto(item) for item in obj.get('phone_numbers')]
        return item_list

    def _get_phone_number_dto(self, item: Dict) -> None:
        phone= phonenumbers.parse(item)
        item_dto = Phone(
            countryCode = phone.country_code,
            phoneNumber= phone.national_number,
            display = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            displayInternational = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        )
        return item_dto   

        




    def _get_profile_Urls(self, obj: Dict) -> None: 
        item_list = [self._get_profile_Url_dto(item) for item in obj.get('profiles')]
        return item_list

    def _get_profile_Url_dto(self, item: Dict) -> None:
        url = [x.strip() for x in item.get('url').split('/')]
        item_dto = URL(
            source = "",
            host = item.get('url'),
            scheme = URLScheme.HTTPS,
            name = url[0],
            raw = URLScheme.HTTPS.name + "://" + item.get('url')
        )
        return item_dto    



        




    def _get_education_data(self, obj: Dict) -> None: 
        item_dto = IndividualEducation(
            education = self._get_education_element(obj)
        )
        return item_dto    

    def _get_education_element(self, obj: Dict) -> None: 
        item_list = [self._get_education_element_dto(item) for item in obj.get('education')]
        return item_list

    def _get_education_element_dto(self, item: Dict) -> None:
        school = item.get('school')
        hasDegree = len(item.get('degrees')) > 0 
        item_dto = EducationElement(
            degree = item.get('degrees')[0] if hasDegree else "",
            school = school["name"],
            started_on = None,
            completed_on = None,
            degree_headline = item.get('degrees')[1] if (hasDegree and len(item.get('degrees')) > 1)  else item.get('degrees')[0] if hasDegree else ""
        )
        return item_dto    



        




    def _get_employement_data(self, obj1: Dict, obj2: Dict) -> None: 
        item_dto = IndividualEmployment(
            employment = self._get_employement_element(obj1, obj2)
        )
        return item_dto    

    def _get_employement_element(self, obj1: Dict, obj2: Dict) -> None: 
        self.employment_list = [self._get_employement_element_dto1(item) for item in obj1.get('experience')]
        self.employment_list.append(self._get_employement_element_dto2(obj2))
        return self.employment_list

    def _get_employement_element_dto1(self, item: Dict) -> None:
        company = item.get('company')
        item_dto = EmploymentElement(
            title = None,
            organization = company['name'],
            industry = company['industry'],
            startedOn = None,
            completedOn = None,
            jobHeadline = None
        )
        return item_dto    

    def _get_employement_element_dto2(self, item: Dict) -> None:
        company = item.get('organization')
        item_dto = EmploymentElement(
            title = None,
            organization = company['name'],
            industry = None,
            startedOn = None,
            completedOn = None,
            jobHeadline = item.get('title')
        )
        return item_dto    
        

    def _get_usernames_list(self, obj: Dict) -> None: 
        self.usernames_list.append(obj.get('linkedin_username'))
        return self.usernames_list
