from dataclasses import dataclass
from typing import Any, List, Optional
from datetime import datetime
import enum

class URLScheme(enum.Enum):
   HTTPS = 1
   HTTP = 2

@dataclass
class Address:
    city: str
    country: str
    state: str
    latitude: float
    longitude: float

@dataclass
class EducationElement:
    degree: Optional[str]
    school: str
    started_on: Optional[datetime]
    completed_on: Optional[datetime]
    degree_headline: Optional[str]

@dataclass
class IndividualEducation:
    education: List[EducationElement]
    
@dataclass
class EmailAddress:
    email_address: str

@dataclass
class EmploymentElement:
    title: Optional[str]
    organization: str
    industry: str
    startedOn: Optional[datetime]
    completedOn: Optional[datetime]
    jobHeadline: str

@dataclass
class IndividualEmployment:
    employment: List[EmploymentElement]

@dataclass
class Phone:
    countryCode: str
    phoneNumber: str
    display: str
    displayInternational: str

@dataclass
class Name:
    first_name: str
    last_name: str
    middle_names: Optional[List[str]]
    prefix: str
    suffix: str
    full_name: str
    full_name_raw: str

@dataclass
class URL:
    source: str
    host: str
    scheme: Any
    name: str
    raw: str

@dataclass
class Individual:
    gc_id: int
    semantic_gc_id: str
    possible_names: List[Name]
    primary_name: Name
    popular_aliases: List[str]
    addresses: List[Address]
    email_addresses: List[EmailAddress]
    tags: List[str]
    phones: List[Phone]
    urls: List[URL]
    education: IndividualEducation
    employment: IndividualEmployment
    usernames: List[str]
