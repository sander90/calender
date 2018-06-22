 #coding=utf-8
import re
import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from calender.items import CalenderItem


class CalenderSpider(scrapy.Spider):
	name = "calender";
	# https://wannianli.tianqi.com/
	start_urls = ["https://wannianli.tianqi.com/huangli/1998-01-01/"]
	def start_requests(self):
		for url in self.start_urls:
			yield SplashRequest(url, self.parse, args={'wait':0.5},endpoint='render.html');


	def parse(self, response):
		# print("=====> %s" %(response.body));
		# //html/body/div[3]/div/div/div[1]/div[1]/div[2]/div[1]
		#yesterday
		sel = response.xpath('//div[@class="btn_rt"]');
		herf = sel.xpath('./a/@href').extract()

		luck_content = response.xpath('//div[@class="luck_content"]/dl');
		print("=====> " , sel )
		print("====> " , herf[0]);
		print("-----> " , len(luck_content));	
		test_a_list = herf[0].split('/');
		herf_t = test_a_list[2];


		calenderItem = CalenderItem();
		calenderItem["time"] = herf_t.encode('utf-8');


		mod_bd = response.xpath('//div[@class="mod_bd"]/dl');
		for dl in mod_bd:
			if dl.xpath('./dt[@class="luck"]'):
				luck = dl.xpath('./dt[@class="luck"]');
				luck_string = self.displayDayLuckThing(luck);
				calenderItem["luck"] = luck_string;

			elif dl.xpath('./dt[@class="bad"]'):
				bad = dl.xpath('./dt[@class="bad"]');
				bad_string = self.displayDayLuckThing(bad);
				calenderItem["bad"] = bad_string;

		if len(luck_content) > 0:

			dataList = [];

			for dl in luck_content:
				time = dl.xpath('./dt/text()').extract()[0];
				print "时间 ", time.encode('utf-8');
				dd_ps = dl.xpath('./dd');
				day_time = CalenderItem();
				day_time["time"] = time.encode('utf-8');
				for dd_p in dd_ps:
					if dd_p.xpath('./p[@class="luck clearfix"]'):
						dd_p_ems = dd_p.xpath('./p[@class="luck clearfix"]/em');
						luck_content = self.displayEmString(dd_p_ems);
						day_time["luck"] = luck_content;
					if dd_p.xpath('./p[@class="bad clearfix"]'):
						dd_p_ems = dd_p.xpath('./p[@class="bad clearfix"]/em');
						bad_content = self.displayEmString(dd_p_ems);
						day_time["bad"] = bad_content;
					if dd_p.xpath('./p/text()'):
						title = dd_p.xpath('./p/text()').extract()[0];
						day_time["title"] = title.encode('utf-8');
				dataList.append(dict(day_time));
			calenderItem["daytime"] = dataList;
			yield calenderItem
			self.err_index = 0;
			# // 正常请求数据，这里错误码归0
			request_url = "https://wannianli.tianqi.com" + herf[0].encode('utf-8');
			print("start URL: ", request_url);
			yield SplashRequest(request_url, self.parse, args={'wait':0.5},endpoint='render.html')
		else: 
			test_list = herf[0].split('/');
			print test_list
			herf_a = test_list[2];
			self.err_index += 1;

			print "error index " , self.err_index;
			if self.err_index < 10 :
				# 错误码生成了，现在继续请求下一页，同时错误码添加
				request_url = "https://wannianli.tianqi.com" + herf[0].encode('utf-8');
				yield SplashRequest(request_url, self.parse, args={'wait': 0.5}, endpoint='render.html')
			else :
				print "结束的时间 ： ", herf_a.encode('utf-8');

	def displayDayLuckThing(self,content):
		luck_p = content.xpath('./p/em');
		return self.displayEmString(luck_p);

	def displayEmString(self, em_p):

		luck_string = ""
		for em in em_p:
			em_text = em.xpath('./text()').extract()[0];
			luck_string = luck_string + em_text.encode('utf-8') + " ";

		return luck_string;










