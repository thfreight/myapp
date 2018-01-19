from simon.models import payee, paytype, pay
import simon.models
from django.db.models import Count


class monthinyear:
	"""This class is used to create months list for whole year according to the year incoming"""
	def __init__(self, year_id):
		self.year_id = year_id
	
	def __str__(self):
		return "Month List in Year " + self.year_id

	def first_last_day(self):
		"""
			Import a year: YYYY
			Output a list from first day to end day of month
			like: [YYYY-1-1, YYYY-1-31, ...., YYYY-12-1, YYYY-12-31]
		"""
		var_first_last_day = []
		for i in range(1, 13):
			end_date_in_month = self.year_id + '-' + str(i) + '-'
			start_date_in_month = end_date_in_month + '1'
			var_first_last_day.append(start_date_in_month)
			if i == 2:
				end_date_in_month = end_date_in_month + '28'
			elif (i == 1) or (i == 3) or (i == 5) or (i==7) or (i==8) or (i==10) or (i==12):
				end_date_in_month = end_date_in_month + '31'
			else:
				end_date_in_month = end_date_in_month + '30'
			var_first_last_day.append(end_date_in_month)
		return var_first_last_day

	def month_list(self):
		"""
			import a year: YYYY
			output a list for each month: [YYYY-01, ...., YYYY-12]
		"""
		var_month_list = []
		for i in range(1,13):
			var_month = str(self.year_id) + '-'
			if i < 10 :
				var_month = var_month +'0' + str(i)
			else:
				var_month = var_month + str(i)
			var_month_list.append(var_month)
		return var_month_list

	def date_makeup(a_date):
		'''
			import a date: YYYY-MM-DD
			output a date: YYYY-MM
		'''
		year, month, day = a_date.split('-')
		if len(month) < 2:
			month = '0'+month
		r_date = year + '-'+month
		return r_date

class month_record:
	def __init__(self, start_day, end_day, payee_id, model_name):
		self.start_day 	= start_day
		self.end_day	= end_day
		self.model_name = model_name
		self.payee_id	= payee_id
	
	def __str__(self):
		return "model = "+ self.model_name

	def retrieve_record(self):
		m=getattr(simon.models, self.model_name).objects.filter(
																pay_date__gte 	= self.start_day, 
																pay_date__lte 	= self.end_day, 
																payee_id 		= self.payee_id)
		table_content=[]
		for t in m:
			table_content.append(t.pay_amount)
		return m #table_content

	def retrieve_head(self):
		'''This method is using for retrieving the table head for payment details'''
		t_year, t_month, t_day 	= self.start_day.split('-')
		t_first_day_year 		= t_year+'-1-1'
		t_last_day_year			= t_year+'-12-31'

		h=getattr(simon.models, self.model_name).objects.filter(payee 			= self.payee_id,
																pay_date__gte 	= t_first_day_year, 
																pay_date__lte 	= t_last_day_year).values('payment_type').annotate(dcount=Count('payment_type'))
		head_list = []
		for hl in h:
			pay_type_inword = paytype.objects.get(id = hl['payment_type']).pay_type
			head_list.append(pay_type_inword)
		head_list.append('PAY DAY')
		return head_list
