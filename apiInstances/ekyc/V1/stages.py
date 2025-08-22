"""Pan"""
try:
    from ekyc.V1.satge_pan.pan import *
except Exception as e:
    print(f"Error in the V1 version pan ->{e}")


#
try:
    from ekyc.V1.stage_customer_details.customer_details import *
except Exception as e:
    print(f"Error in the V1 version customer_details ->{e}")

try:
    from ekyc.V1.stage_kra_or_aadhaar.kra_or_aadhaar import *
except Exception as e:
    print(f"Error in the V1 version kra_or_aadhaar ->{e}")


#
try:
    from ekyc.V1.stage_segments.segments import *
except Exception as e:
    print(f"Error in the V1 version segments ->{e}")
#
try:
    from ekyc.V1.stage_t_and_c.t_and_c import *
except Exception as e:
    print(f"Error in the V1 version t_and_c ->{e}")
#
try:
    from ekyc.V1.stage_nominee.update_nominee import *
except Exception as e:
    print(f"Error in the V1 version nominee ->{e}")
#
try:
    from ekyc.V1.stage_document.upload.client_upload import *
except Exception as e:
    print(f"Error in the V1 version client_upload ->{e}")
#
try:
    from ekyc.V1.stage_document.delete.client_delete import *
except Exception as e:
    print(f"Error in the V1 version client_delete ->{e}")
#
try:
    from ekyc.V1.stage_document.complete_document_stage import *
except Exception as e:
    print(f"Error in the V1 version complete_document_stage ->{e}")

try:
    from ekyc.V1.stage_ipv.ipv import *
except Exception as e:
    print(f"Error in the V1 version ipv ->{e}")
#
try:
    from ekyc.V1.stage_bank.penny_drop_bank_update import *
except Exception as e:
    print(f"Error in the V1 version bank_update ->{e}")

try:
    from ekyc.V1.stage_bank.reverse_penny_drop_request import *
except Exception as e:
    print(f"Error in the V1 version bank_update ->{e}")

try:
    from ekyc.V1.stage_bank.reverse_penny_drop_bank_status import *
except Exception as e:
    print(f"Error in the V1 version bank_update ->{e}")

try:
    from ekyc.V1.stage_bank.save_reverse_penny_drop_details import *
except Exception as e:
    print(f"Error in the V1 version bank_update ->{e}")
try:
    from ekyc.V1.stage_kra_or_aadhaar.digilocker.create_consent import *
except Exception as e:
    print(f"Error in the V1 version digilocker create consent ->{e}")

try:
    from ekyc.V1.stage_kra_or_aadhaar.digilocker.get_digilocker_status import *
except Exception as e:
    print(f"Error in the V1 version digilocker update digilocker data ->{e}")

try:
    from ekyc.V1.stage_kra_or_aadhaar.digilocker.update_digilocker_data import *
except Exception as e:
    print(f"Error in the V1 version digilocker update digilocker data ->{e}")

try:
    from ekyc.V1.stage_esign.esign_fill_pdf import *
except Exception as e:
    print(f"Error in the V1 version esign fil pdf ->{e}")

try:
    from ekyc.V1.stage_esign.esign_consent import *
except Exception as e:
    print(f"Error in the V1 version esign consent ->{e}")

try:
    from ekyc.V1.stage_esign.get_signed_document import *
except Exception as e:
    print(f"Error in the V1 version esign get signed document ->{e}")

try:
    from ekyc.V1.account_aggregator.create_consent import *
except Exception as e:
    print(f"Error in the V1 version esign get signed document ->{e}")

try:
    from ekyc.V1.account_aggregator.fetch_aa_data import *
except Exception as e:
    print(f"Error in the V1 version esign get signed document ->{e}")

try:
    from ekyc.V1.stage_document.doc_pan_fetch import *
except Exception as e:
    print(f"Error in the V1 version esign get signed document ->{e}")

try:
    from ekyc.V1.stage_document.upload.get_mongodb_client_document import *
except Exception as e:
    print(f"Error in the V1 version get client document->{e}")

try:
    from ekyc.V1.cams.cams_account_aggregator import  *
except Exception as e:
    print(f"Error in the V1 version create cams account aggregator consent->{e}")

try:
    from ekyc.V1.cams.fetch_aa_data import  *
except Exception as e:
    print(f"Error in the V1 version get aa data->{e}")