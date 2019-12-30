import dos2de_common as common

template_goal = """Version 1
SubGoalCombiner SGC_AND
INITSECTION
/* This script is auto-generated via {file} in DivinityTools*/
KBSECTION
{code}\nEXITSECTION
ENDEXITSECTION"""

template_redirection = """
QRY
{function_header}
AND
NOT DB_LeaderLib_DialogOverride_Redirection_BlacklistedDialog(_Dialog, {speakers})
AND
LeaderLib_DialogOverride_QRY_CanRedirect(_Dialog)
AND
LeaderLib_DialogOverride_QRY_CanRedirectObject({speaker})
AND
NOT LeaderLib_DialogOverride_QRY_DialogIsPlayerStarted({speakers})
AND
NOT LeaderLib_DialogOverride_QRY_SpeakersHaveAvatar({speakers})
AND
LeaderLib_DialogOverride_QRY_Internal_GetRedirectionTarget(_Dialog, {speaker})
AND
DB_LeaderLib_DialogOverride_Temp_RedirectionTarget(_Dialog, (GUIDSTRING)_Target, {speaker})
THEN
DB_LeaderLib_DialogOverride_Temp_Order(_Dialog, {order});
"""

#LeaderLib_DialogOverride_QRY_GetRedirectionTarget((STRING)_Dialog, (GUIDSTRING)_Speaker1, (GUIDSTRING)_Speaker2, (GUIDSTRING)_Speaker3, (GUIDSTRING)_Speaker4, (GUIDSTRING)_Speaker5, (GUIDSTRING)_Speaker6)

output_str = ""
for start_count in range(6,1,-1):
	output_str += '//REGION GET_REDIRECTION_TARGET_{}'.format(start_count)
	for num in range(start_count, 1, -1):
		speaker = "_Speaker{}".format(num)
		params = ""
		for i in range(1, start_count+1):
			params += "(GUIDSTRING)_Speaker{}".format(i)
			if i < start_count: params += ", "
		function_header = "LeaderLib_DialogOverride_QRY_GetRedirectionTarget((STRING)_Dialog, {})".format(params)
		speakers = ""
		for i in range(1, start_count+1):
			speakers += "_Speaker{}".format(i)
			if i < start_count: speakers += ", "
		order = ""
		for i in range(1, start_count+1):
			if i == num:
				order += "_Target"
			else:
				order += "_Speaker{}".format(i)
			if i < start_count: order += ", "
		output_str += template_redirection.format(function_header=function_header, speaker=speaker, order=order, speakers=speakers)
	output_str += '//END_REGION\n\n'

from pathlib import Path
common.clipboard_copy(template_goal.format(code=output_str, file=Path(__file__).stem))