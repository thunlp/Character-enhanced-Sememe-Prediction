#Make sure that you have run SPSE.sh, SPWE.sh, SPWCF.sh, and SPCSE.sh
python Ensemble_model.py model_SPWE model_SPSE 0.3125 hownet.txt_test output_Ensemble_SPWE_SPSE_test model_Ensemble_SPWE_SPSE_test 
python Ensemble_model.py model_SPWCF_test model_SPCSE_test 4.0 hownet.txt_test output_Ensemble_SPWCF_SPCSE_test model_Ensemble_SPWCF_SPCSE_test
python Ensemble_model.py model_Ensemble_SPWE_SPSE_test model_Ensemble_SPWCF_SPCSE_test 1.0 hownet.txt_test output_CSP model_CSP
python scorer.py output_CSP hownet.txt_answer

