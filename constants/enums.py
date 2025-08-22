"""DOC FORMATS"""
FORMAT_PNG = "image/png"
FORMAT_JPEG = "image/jpeg"
FORMAT_JPG = "image/jpg"
FORMAT_HEIC = 'image/heic'
FORMAT_WEBP = "image/webp"
FORMAT_PDF = "application/pdf"

"""END POINTS"""
EKYC_BASE_ENDPOINT = "/v1/api/ekyc/"

"""EKYC Stage Sequence"""
EKYC_STAGE_MOBILE = "mobile"
EKYC_STAGE_EMAIL = "email"
EKYC_STAGE_PAN = "pan"
EKYC_STAGE_KRA_OR_AADHAAR = "kra_or_aadhaar"
EKYC_STAGE_CUSTOMER_DETAILS = "customer_details"
EKYC_STAGE_SEGMENT = "segment"
EKYC_STAGE_BANK = "bank"
EKYC_STAGE_T_AND_C = "t_and_c"
EKYC_STAGE_NOMINEE = "nominee"
EKYC_STAGE_DOCUMENT_UPLOAD = "document_upload"
EKYC_STAGE_IPV = "ipv"
EKYC_STAGE_E_SIGN = "esign"
EKYC_STAGE_CONGRATULATIONS = 'congratulations'
EKYC_STAGE_APPROVED = 'application_approved'

"""SETU DIGILOCKER DOCUMENT TYPES"""
SETU_DOC_PANCARD = 'PANCR'

"""DOCUMENT REFERENCES"""
DOC_PANCARD_REF = "pancard"
DOC_PANCARD_PURPOSE = "pancard"
DOC_PANCARD_FILE_FORMAT = FORMAT_PDF

DOC_AADHAAR_REF = "aadhaar"
DOC_AADHAAR_PURPOSE = "aadhaar"
DOC_AADHAAR_FILE_FORMAT = FORMAT_JPEG

DOC_SIGNATURE_PURPOSE = "signature"
DOC_IPV_PURPOSE = 'ipv'
DOC_INCOME_PROOF_PURPOSE = "income_proof"
DOC_BANK_PROOF_PURPOSE = "bank_proof"
DOC_ESIGN_PURPOSE = 'e_sign_pdf'
DOC_TEMP_ESIGN_PURPOSE = 'temp_esign_pdf'
DOC_NOMINEE_ONE_PURPOSE = 'nominee_proof1'
DOC_NOMINEE_TWO_PURPOSE = 'nominee_proof2'
DOC_NOMINEE_THREE_PURPOSE = 'nominee_proof3'
DOC_REF_BANK_STATEMENT = 'bank_statement'

"""Redirect End path"""
DIGILOCKER_END_PATH = "ekyc_aadhaar"

"""Mongodb Master Object Ids"""

"""KRA Values"""
KRA_NEW = 'KRA_NEW'
KRA_EXISTING = 'KRA_EXISTING'
KRA_MODIFIED = 'KRA_MODIFIED'

"""Stage Status Values"""
STAGE_OPEN = "open"
STAGE_COMPLETED = "completed"
STAGE_REJECTED = 'rejected'
