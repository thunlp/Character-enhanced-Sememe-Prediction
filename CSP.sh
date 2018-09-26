#Make sure that you have run SPSE.sh, SPWE.sh, SPWCF.sh, and SPCSE.sh
python3 pickle_version_change.py
python Ensemble_model_external.py model_SPWE model_SPSE 0.3125 hownet.txt_test_input output_Ensemble_SPWE_SPSE_test model_Ensemble_SPWE_SPSE_test 
python Ensemble_model_internal.py model_SPWCF_test model_SPCSE_test 4.0 hownet.txt_test_input output_Ensemble_SPWCF_SPCSE_test model_Ensemble_SPWCF_SPCSE_test
python Ensemble_model_CSP.py model_Ensemble_SPWE_SPSE_test model_Ensemble_SPWCF_SPCSE_test 1.0 hownet.txt_test_input output_CSP model_CSP
python scorer.py output_CSP hownet.txt_test_answer

