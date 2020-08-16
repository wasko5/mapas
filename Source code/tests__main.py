# MUltiple tests corrections and FOrmatted tables Software (MUFOS)
# Copyright (C) 2020  Nikolay Petrov, Vasil Atanasov, & Trevor Thompson
import tests_corrections
import tests_raw_correlations
import tests_raw_mr
import tests_raw_indttest
import tests_raw_pairttest
import tests_summ_indttest
import tests_spss_correlations
import tests_spss_mr
import tests_spss_indttest
import tests_spss_pairttest
import tests_csv
import tests_APAtables

if __name__ == "__main__":
	tests_corrections.main()
	tests_raw_correlations.main()
	tests_raw_mr.main()
	tests_raw_indttest.main()
	tests_raw_pairttest.main()
	tests_summ_indttest.main()
	tests_spss_correlations.main()
	tests_spss_mr.main()
	tests_spss_indttest.main()
	tests_spss_pairttest.main()
	tests_csv.main()
	tests_APAtables.main()