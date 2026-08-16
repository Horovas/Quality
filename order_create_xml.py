import random
import requests
import xml.etree.ElementTree as ET
from faker import Faker

fake = Faker('ru_EN')


url = "http://test.test.ru/test/test/TestService"
session = "test_session"
idDepartment = 932608
idsubdivision_1 = 44183446
idsubdivision_2 = 44183447
idsubdivision_3 = 44183448
idprice_category = 617690
price_1 = 777
price_2 = 526
price_3 = 882
extra_1 = 77
extra_2 = 52
extra_3 = 88
total = price_1 + price_2 + price_3 + extra_1 + extra_2 + extra_3
first_name_1 = fake.first_name_male()
last_name_1 = fake.last_name_male()
first_name_2 = fake.first_name_male()
last_name_2 = fake.last_name_male()
first_name_3 = fake.first_name_male()
last_name_3 = fake.last_name_male()

requestUid = random.randrange(100000000)
lockKey = random.randrange(100000)

doc_enum = [
    "DRIVERS_LICENSE",
    "PASSPORT",
    "NATIONAL_ID_CARD",
    "BIRTH_CERTIFICATE",
    "MARRIAGE_CERTIFICATE",
    "UTILITY_BILL",
    "BANK_STATEMENT",
    "TAX_RETURN",
    "SOCIAL_SECURITY_CARD",
    "MILITARY_ID",
    "HEALTH_INSURANCE_CARD",
    "STUDENT_ID",
    "RESIDENCE_PERMIT",
    "VOTER_REGISTRATION_CARD",
    "EMPLOYMENT_CONTRACT",
    "VEHICLE_REGISTRATION",
    "LAND_DEED",
    "DIPLOMA_CERTIFICATE",
    "MEDICAL_RECORD",
    "POWER_OF_ATTORNEY",
]

options = {"Content-Type": "text/xml; charset=UTF-8"}


def subdivision_lock_func(
    session: str,
    requestUid: int,
    idDepartment: int,
    idsubdivision_1: int,
    idsubdivision_2: int,
    idsubdivision_3: int,
    idprice_category: int,
    price_1: int,
    price_2: int,
    price_3: int,
    extra_1: int,
    extra_2: int,
    extra_3: int,
    lockKey: int,
):
    """Locking object"""
    response = requests.post(
        url,
        headers=options,
        data=f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tic="http://some_url">
               <soapenv:Header/>
               <soapenv:Body>
                  <tic:subdivisionLock>
                     <sessionUUID>{session}</sessionUUID>
                     <requestUid>{requestUid}</requestUid>
                     <!--1 or more repetitions:-->
                     <subdivisionLocks>
                        <idDepartment>{idDepartment}</idDepartment>
                        <idsubdivision>{idsubdivision_1}</idsubdivision>
                        <idprice_category>{idprice_category}</idprice_category>
                        <price>
                           <price>{price_1}</price>
                           <extra>{extra_1}</extra>
                        </price>
                     </subdivisionLocks>
                     <subdivisionLocks>
                        <idDepartment>{idDepartment}</idDepartment>
                        <idsubdivision>{idsubdivision_2}</idsubdivision>
                        <idprice_category>{idprice_category}</idprice_category>
                        <price>
                           <price>{price_2}</price>
                           <extra>{extra_2}</extra>
                        </price>
                     </subdivisionLocks>
                     <subdivisionLocks>
                        <idDepartment>{idDepartment}</idDepartment>
                        <idsubdivision>{idsubdivision_3}</idsubdivision>
                        <idprice_category>{idprice_category}</idprice_category>
                        <price>
                           <price>{price_3}</price>
                           <extra>{extra_3}</extra>
                        </price>
                     </subdivisionLocks>

                     <lockKey>KEY{lockKey}</lockKey>
                  </tic:subdivisionLock>
               </soapenv:Body>
            </soapenv:Envelope>
            """,
    )

    root = ET.fromstring(response.text)

    for child in root.iter("*"):
        print(child.tag, child.text)

    print()

    return


def order_create_func(
    session: str,
    requestUid: int,
    idDepartment: int,
    idsubdivision_1: int,
    idsubdivision_2: int,
    idsubdivision_3: int,
    lockKey: int,
    doc_enum: list,
    first_name_1: str,
    last_name_1: str,
    first_name_2: str,
    last_name_2: str,
    first_name_3: str,
    last_name_3: str,
):
    """Creating order"""
    response = requests.post(
        url,
        headers=options,
        data=f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tic="http://some_url">
               <soapenv:Header/>
               <soapenv:Body>

                  <tic:orderCreate>
                     <sessionUUID>{session}</sessionUUID>
                     <requestUid>{requestUid+1}</requestUid>
                     <idClient>1</idClient>
                     <basket>
                        <!--1 or more repetitions:-->
                        <subdivisions>
                            <idDepartment>{idDepartment}</idDepartment>
                            <idsubdivision>{idsubdivision_1}</idsubdivision>
                        </subdivisions>
                        <subdivisions>
                            <idDepartment>{idDepartment}</idDepartment>
                            <idsubdivision>{idsubdivision_2}</idsubdivision>
                        </subdivisions>
                        <subdivisions>
                            <idDepartment>{idDepartment}</idDepartment>
                            <idsubdivision>{idsubdivision_3}</idsubdivision>
                        </subdivisions>
                        
                        <!--Zero or more repetitions:-->
                        <spectators>
                           <documentNumber>{requestUid+99999}</documentNumber>
                           <documentType>{random.choice(doc_enum)}</documentType>
                           <email>testmail_1@gmail.com</email>
                           <name>{first_name_1}</name>
                           <DepartmentId>{idDepartment}</DepartmentId>
                           <subdivisionId>{idsubdivision_2}</subdivisionId>
                           <phone>+79450001112</phone>
                           <spectatorExternalDitId>soap_53516</spectatorExternalDitId>
                           <surname>{last_name_1}</surname>
                           <ticketPersonalDataId>6268567</ticketPersonalDataId>
                        </spectators>
                        <spectators>
                           <documentNumber>{requestUid+99999}</documentNumber>
                           <documentType>{random.choice(doc_enum)}</documentType>
                           <email>testmail_2@gmail.com</email>
                           <name>{first_name_2}</name>
                           <DepartmentId>{idDepartment}</DepartmentId>
                           <subdivisionId>{idsubdivision_2}</subdivisionId>
                           <phone>+79450001113</phone>
                           <spectatorExternalDitId>soap_53516</spectatorExternalDitId>
                           <surname>{last_name_2}</surname>
                           <ticketPersonalDataId>6268567</ticketPersonalDataId>
                        </spectators>
                        <spectators>
                           <documentNumber>{requestUid+99999}</documentNumber>
                           <documentType>{random.choice(doc_enum)}</documentType>
                           <email>testmail_3@gmail.com</email>
                           <name>{first_name_3}</name>
                           <DepartmentId>{idDepartment}</DepartmentId>
                           <subdivisionId>{idsubdivision_3}</subdivisionId>
                           <phone>+79450001114</phone>
                           <spectatorExternalDitId>soap_53516</spectatorExternalDitId>
                           <surname>{last_name_3}</surname>
                           <ticketPersonalDataId>6268567</ticketPersonalDataId>
                        </spectators>


                     </basket>
                     <lockKey>KEY{lockKey}</lockKey>
                     <withEtickets>true</withEtickets>
                     <expireTime>?</expireTime>
                     <utmId>?</utmId>
                     <siteId>?</siteId>
                     
                  </tic:orderCreate>
               </soapenv:Body>
            </soapenv:Envelope>
            """,
    )

    root = ET.fromstring(response.text)

    for child in root.iter("*"):
        print(child.tag, child.text)
        if child.tag == "idOrder":
            idOrder = int(child.text)

    print()

    return idOrder


def order_print_objects_func(session: str, requestUid: int, idOrder: int):
    """Printing objects"""
    response = requests.post(
        url,
        headers=options,
        data=f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tic="http://some_url">
               <soapenv:Header/>
               <soapenv:Body>
                  <tic:orderPrintEtickets>
                     <sessionUUID>{session}</sessionUUID>
                     <requestUid>{requestUid+2}</requestUid>
                     <idOrder>{idOrder}</idOrder>
                     <!--Optional:-->
                     <specialPayment>?</specialPayment>
                  </tic:orderPrintEtickets>
               </soapenv:Body>
            </soapenv:Envelope>
            """,
    )

    root = ET.fromstring(response.text)

    for child in root.iter("*"):
        print(child.tag, child.text)

    print()

    return


def payment_func(session: str, requestUid: int, idOrder: int, total: int):
    """Payment process"""
    response = requests.post(
        url,
        headers=options,
        data=f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tic="http://some_url">
               <soapenv:Header/>
               <soapenv:Body>
                   <tic:ticketOperationsOrderPay>
                     <sessionUUID>{session}</sessionUUID>
                     <requestUid>{requestUid+3}</requestUid>
                     <idOrder>{idOrder}</idOrder>
                     <kkmNo>12</kkmNo>
                       <payment>
                        <mean>card</mean>
                        <!--Optional:-->
                        <providerCode>sberbank</providerCode>
                        <rrn>{requestUid}</rrn>
                        <sum>{total}</sum>
                        <transactionId>transaction_{requestUid}</transactionId>
                     </payment>
                  </tic:ticketOperationsOrderPay>
               </soapenv:Body>
            </soapenv:Envelope>
            """,
    )

    root = ET.fromstring(response.text)

    for child in root.iter("*"):
        print(child.tag, child.text)

    print()

    return


def get_info_order_func(session: str, idOrder: int):
    """Get Info Order"""
    response = requests.post(
        url,
        headers=options,
        data=f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tic="http://some_url">
               <soapenv:Header/>
               <soapenv:Body>
                  <tic:getInfoOrder>
                     <sessionUUID>{session}</sessionUUID>
                     <orderId>{idOrder}</orderId>
                     <pin></pin>
                     <includesubdivisions>true</includesubdivisions>
                     <includePayments>true</includePayments>
                     <!--Optional:-->
                     <extraOptions>?</extraOptions>
                  </tic:getInfoOrder>
               </soapenv:Body>
            </soapenv:Envelope>
            """,
    )

    root = ET.fromstring(response.text)

    for child in root.iter("*"):
        print(child.tag, child.text)

    print()

    return


def set_spectator_info_func(
    session: str, 
    idOrder: int,
    doc_enum: list,
    idDepartment: int, 
    idsubdivision_1: int,
    idsubdivision_2: int,
    idsubdivision_3: int,
    first_name_1: str,
    last_name_1: str,
    first_name_2: str,
    last_name_2: str,
    first_name_3: str,
    last_name_3: str,
):
    """Set User Info"""
    response = requests.post(
        url,
        headers=options,
        data=f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tic="http://some_url">
               <soapenv:Header/>
               <soapenv:Body>
               
                  <tic:setSpectatorsInfo>
                     <sessionUUID>{session}</sessionUUID>
                     <orderId>{idOrder}</orderId>
                     <!--Zero or more repetitions:-->
                     <spectatorsInfo>
                        <documentNumber>1133467</documentNumber>
                        <documentType>NATIONAL_ID_CARD</documentType>
                        <email>testme_1@gmail.com</email>
                        <name>{first_name_1}</name>
                        <DepartmentId>{idDepartment}</DepartmentId>
                        <subdivisionId>{idsubdivision_1}</subdivisionId>
                        <phone>+760323465931</phone>
                        <spectatorExternalDitId>soap_777</spectatorExternalDitId>
                        <surname>{last_name_1}</surname>
                        <ticketPersonalDataId>432143</ticketPersonalDataId>
                     </spectatorsInfo>

                     <spectatorsInfo>
                        <documentNumber>1133467</documentNumber>
                        <documentType>PASSPORT</documentType>
                        <email>testme_2@gmail.com</email>
                        <name>{first_name_2}</name>
                        <DepartmentId>{idDepartment}</DepartmentId>
                        <subdivisionId>{idsubdivision_2}</subdivisionId>
                        <phone>+760323465916</phone>
                        <spectatorExternalDitId>soap_777</spectatorExternalDitId>
                        <surname>{last_name_2}</surname>
                        <ticketPersonalDataId>432143</ticketPersonalDataId>
                     </spectatorsInfo>

                     <spectatorsInfo>
                        <documentNumber>1133467</documentNumber>
                        <documentType>VOTER_REGISTRATION_CARD</documentType>
                        <email>testme_3@gmail.com</email>
                        <name>{first_name_3}</name>
                        <DepartmentId>{idDepartment}</DepartmentId>
                        <subdivisionId>{idsubdivision_3}</subdivisionId>
                        <phone>+760323465918</phone>
                        <spectatorExternalDitId>soap_777</spectatorExternalDitId>
                        <surname>{last_name_3}</surname>
                        <ticketPersonalDataId>432143</ticketPersonalDataId>
                     </spectatorsInfo>
                     
                  </tic:setSpectatorsInfo>
               </soapenv:Body>
            </soapenv:Envelope>
            """,
    )

    root = ET.fromstring(response.text)

    for child in root.iter("*"):
        print(child.tag, child.text)

    print()

    return


# response_info_order = requests.post(url, data=getInfoOrder, headers=options)
# root = ET.fromstring(response_info_order.text)

# for child in root.iter("*"):
#    print(child.tag, child.text)

# print()


def main():

    subdivision_lock_func(
        session,
        requestUid,
        idDepartment,
        idsubdivision_1,
        idsubdivision_2,
        idsubdivision_3,
        idprice_category,
        price_1,
        price_2,
        price_3,
        extra_1,
        extra_2,
        extra_3,
        lockKey
    )

    idOrder = order_create_func(
        session,
        requestUid,
        idDepartment,
        idsubdivision_1,
        idsubdivision_2,
        idsubdivision_3,
        lockKey,
        doc_enum,
        first_name_1,
        last_name_1,
        first_name_2,
        last_name_2,
        first_name_3,
        last_name_3
    )

    order_print_etickets_func(session, requestUid, idOrder)

    payment_func(session, requestUid, idOrder, total)

    get_info_order_func(session, idOrder)

    set_spectator_info_func(
        session, 
        idOrder, 
        doc_enum, 
        idDepartment, 
        idsubdivision_1,
        idsubdivision_2,
        idsubdivision_3,
        first_name_1,
        last_name_1,
        first_name_2,
        last_name_2,
        first_name_3,
        last_name_3
    )

    get_info_order_func(session, idOrder)


if __name__ == "__main__":

    main()
