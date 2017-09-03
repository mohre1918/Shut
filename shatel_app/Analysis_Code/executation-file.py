from copyfile import *
from period_result2Postgres import *
from duration_per_operator_result2Postgres import *
from duration_per_province_result2Postgres import *
mgws = ['MGW_HMN_EALI', 'MGW_KOR_SAN', 'MGW_YZD_SADQ', 'MGW_QOM_QOM', 'MGW_ARB_PC', 'MGW_ZNJ_PC', 'MGW_SMN_AMLO', 'MGW_OUR_MDRS', 'MGW_KRM_VASR', 'MGW_BOU_BHMN', 'MGW_HAM_TAHER', 'MGW_MZN_EMAM2', 'MGW_TEH_SC21','MGW_FRS_VALI', 'MGW_ESF_EMAM1', 'MGW_ESF_EMAM2', 'MGW_ABZ_KRJ', 'MGW_KHZ_VALI2', 'MGW_KHZ_VALI1', 'MGW_CMB_PC', 'MGW_MZN_EMAM1','MGW_GLN_GLSR', 'MGW_GRN_EMAM', 'MGW_KHS_PC', 'MGW_TEH_SC22','MGW_TAB_RHMI', 'MGW_TEH_ISC2', 'MGW_HAM_TAHER2', 'MGW_KHR_FRSH', 'MGW_KHR_FRSH2']
prefixes = ['76', '87', '35', '25', '45', '24', '23', '44', '34', '77', '81', '11', '21','71', '11', '31', '31', '26', '61','61', '38', '11','13', '17', '58','21', '41', '21','81', '51', '51']
operators = ['shatel', 'mci', 'mtn', 'rtl', 'TCI', 'TIC', 'Undefined']
dates=["oneDay", "oneWeek", "oneMonth","threeMonth","sixMonth", "oneYear"]
deltas = [-1 , -7, -30,-90,-180,-365]



##################### Downloads MediaGateway files ####################
# execfile("ftpdownload.py")
# ##################### Edit files and Copy to Databases ################
# for i in range(0,len(mgws)):
#     COPY(mgws[i], prefixes[i])

#################### Copy period result 2 postgres ####################

period_data_generate(mgws, operators)

################## Copy duration per operator result 2 postgres #####
duration_per_operator_data_generate(mgws,dates, deltas)

################## Copy duration and crinfo per Province result 2 postgres ###########
Outgoing_duration_per_operator_data_generate(mgws, operators, dates, deltas)
Incommming_duration_per_operator_data_generate(mgws, operators, dates, deltas)


