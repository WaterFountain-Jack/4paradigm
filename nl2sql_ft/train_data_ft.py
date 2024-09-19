all_data = [
    {'query': '2022年华夏银行的存货减少了多少？', 'sql': "SELECT\nsum(inventory_decrease) AS total_inventory_decrease \nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date) = 2022 AND b.name = '华夏银行'", 'order': False
    },
    {'query': '2022年上港集团是否有信用减值损失？', 'sql': "SELECT\nIFNULL(SUM(credit_impairment_loss), 0) AS total_credit_impairment_loss\nFROM\ncash_flow_CN_STOCK_A t1\nINNER JOIN basic_info_CN_STOCK_A t2 ON t1.instrument = t2.instrument \nAND t2.name = '上港集团' \nWHERE\nYEAR ( report_date )= '2022'", 'order': False
    },
    {'query': '2022年格力电器的现金流量表中的经营活动现金流量净额是多少？', 'sql': "SELECT\nIFNULL( sum( sub_total_of_ci_from_oa ), 0 ) - IFNULL( sum( sub_total_of_cos_from_oa ), 0 ) AS 经营活动现金流量净额 \nFROM\ncash_flow_CN_STOCK_A t1\nINNER JOIN basic_info_CN_STOCK_A t2 ON t1.instrument = t2.instrument \nAND t2.NAME = '格力电器' \nWHERE\nYEAR ( report_date )= '2022'", 'order': False
    },
    {'query': '2022年华夏银行和格力电器哪家公司的经营活动现金流入小计更高？', 'sql': "SELECT\nname,sub_total_of_ci_from_oa \nFROM\n(\nSELECT\nb.name,\nsum( a.sub_total_of_ci_from_oa ) AS sub_total_of_ci_from_oa \nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022 AND b.name IN ( '格力电器', '华夏银行' ) \nGROUP BY\nb.name \n) k \nORDER BY\nk.sub_total_of_ci_from_oa DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年华夏银行的现金等价物的期末余额是多少？', 'sql': "SELECT\nIFNULL( sum( si_final_balance_of_cce ), 0 ) AS si_final_balance_of_cce \nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022 \nAND b.NAME = '华夏银行'", 'order': False
    },
    {'query': '2022年格力电器的偿还债务支付的现金是多少？', 'sql': "SELECT\nIFNULL( sum( cash_pay_for_debt ),0) as cash_pay_for_debt\nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date ) = 2022 AND b.company_name = '格力电器'", 'order': False
    },
    {'query': '2022年格力电器的偿还债务支付的现金是多少？', 'sql': "SELECT\nIFNULL( sum(a.cash_pay_for_debt ),0) as cash_pay_for_debt\nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date ) = 2022 AND b.name = '格力电器'", 'order': False
    },
    {'query': '2022年华夏银行的现金等价物的期初余额是多少？', 'sql': "SELECT\nIFNULL( sum( initial_balance_of_cce ),0) as initial_balance_of_cce\nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument WHERE\nYEAR (a.report_date ) = 2022 AND b.name = '华夏银行'", 'order': False
    },
    {'query': '2022年格力电器的支付利息、手续费及佣金的现金是多少？', 'sql': "SELECT\nIFNULL( sum( cash_paid_for_interests_etc ),0) as cash_paid_for_interests_etc\nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date ) = 2022 AND b.name = '格力电器'", 'order': False
    },
    {'query': '2022年华夏银行的质押贷款净增加额是多少？', 'sql': "SELECT\nIFNULL( sum( net_add_in_pledge_loans ),0) as net_add_in_pledge_loans\nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date ) = 2022 AND b.name = '华夏银行'", 'order': False
    },
    {'query': '2022年格力电器的投资支付的现金是多少？', 'sql': "SELECT\nIFNULL( sum( invest_paid_cash ),0) as invest_paid_cash\nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date ) = 2022 AND b.name = '格力电器'", 'order': False
    },
    {'query': '2022年华夏银行的取得投资收益收到的现金是多少？', 'sql': "SELECT\nIFNULL( sum( invest_income_cash_received ), 0 ) AS invest_income_cash_received \nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022 \nAND b.NAME = '华夏银行'", 'order': False
    },
    {'query': '2022年格力电器的现金及现金等价物净增加额是多少？', 'sql': "SELECT\nIFNULL( sum( net_increase_in_cce ),0) AS net_increase_in_cce \nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022 \nAND b.NAME = '格力电器'", 'order': False
    },
    {'query': '2022年华夏银行的筹资活动现金流入小计是多少？', 'sql': "SELECT\nIFNULL( sum(a.sub_total_of_ci_from_fa ),0) as sub_total_of_ci_from_fa\nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date ) = 2022 AND b.name = '华夏银行'", 'order': False
    },
    {'query': '2022年格力电器的筹资活动现金流出小计是多少？', 'sql': "SELECT\nsum( a.sub_total_of_cos_from_fa ) AS sub_total_of_ci_from_fa \nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022 AND b.name = '格力电器'", 'order': False
    },
    {'query': '2022年华夏银行和格力电器哪家公司的筹资活动现金流入小计更高？', 'sql': "SELECT\nNAME,\nsub_total_of_ci_from_fa \nFROM\n(\nSELECT\nb.NAME,\nIFNULL(sum( a.sub_total_of_ci_from_fa ),0) AS sub_total_of_ci_from_fa \nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022 \nAND b.NAME IN ( '格力电器', '华夏银行' ) \nGROUP BY\nb.NAME \n) k \nORDER BY\nk.sub_total_of_ci_from_fa DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年华夏银行的支付其他与经营活动有关的现金是多少？', 'sql': "SELECT\nIFNULL( sum( other_cash_paid_related_to_oa ),0) as other_cash_paid_related_to_oa\nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date ) = 2022 AND b.name = '华夏银行'", 'order': False
    },
    {'query': '2022年格力电器的支付其他与经营活动有关的现金是多少？', 'sql': "SELECT\nIFNULL( sum( other_cash_paid_related_to_oa ),0) as other_cash_paid_related_to_oa\nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date ) = 2022 AND b.name = '格力电器'", 'order': False
    },
    {'query': '2022年华夏银行和格力电器哪家公司的支付其他与经营活动有关的现金更多？', 'sql': "SELECT\nname,other_cash_paid_related_to_oa\nFROM\n(\nSELECT\nname,\nIFNULL( sum( other_cash_paid_related_to_oa ),0) AS other_cash_paid_related_to_oa \nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022 AND b.name IN ( '格力电器', '华夏银行' )\nGROUP BY\nb.name \n) k \nORDER BY\nk.other_cash_paid_related_to_oa DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年华夏银行的偿还债务支付的现金是多少？', 'sql': "SELECT\nIFNULL( sum( cash_pay_for_debt ) ,0) as cash_pay_for_debt\nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date ) = 2022 AND b.name = '华夏银行'", 'order': False
    },
    {'query': '2022年格力电器的偿还债务支付的现金是多少？', 'sql': "SELECT\nIFNULL( sum( cash_pay_for_debt ),0) as cash_pay_for_debt\nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date ) = 2022 AND b.company_name = '格力电器'", 'order': False
    },
    {'query': '2022年格力电器的偿还债务支付的现金是多少？', 'sql': "SELECT\nIFNULL( sum(a.cash_pay_for_debt ),0) as cash_pay_for_debt\nFROM\ncash_flow_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date ) = 2022 AND b.name = '格力电器'", 'order': False
    },
    {'query': '2022年华夏银行的总利润是多少？', 'sql': "SELECT\nIFNULL( sum( total_profit ),0) as total_profit\nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date ) = 2022 AND b.name = '华夏银行'", 'order': False
    },
    {'query': '在所有上海的公司中，哪家公司的投资收益最高？', 'sql': "SELECT\ncompany_name,\nIFNULL( sum( invest_income ), 0 ) AS invest_income \nFROM\nincome_CN_STOCK_A t1\nINNER JOIN basic_info_CN_STOCK_A t2 ON t1.instrument = t2.instrument \nAND t2.company_province = '上海' \nGROUP BY\nt2.company_name \nORDER BY\ninvest_income DESC \nLIMIT 1", 'order': False
    },
    {'query': '比较广东的格力电器和比亚迪，哪家公司在2022年的手续费及佣金收入更高？', 'sql': "SELECT\ncompany_name,\nIFNULL(sum( fee_and_commi_income ),0) AS fee_and_commi_income \nFROM\nincome_CN_STOCK_A t1\nINNER JOIN basic_info_CN_STOCK_A t2 ON t1.instrument = t2.instrument \nAND t2.name IN ( '格力电器', '比亚迪' ) \nAND t2.company_province = '广东省' \nWHERE\nYEAR ( report_date )= '2022' \nGROUP BY\nt2.company_name \nORDER BY\nfee_and_commi_income DESC \nLIMIT 1", 'order': False
    },
    {'query': '长虹能源和同享科技在2022年的营业总成本中，哪家公司的财务费用更高？', 'sql': "SELECT\nNAME,\nfinancing_expenses \nFROM\n(\nSELECT\nb.NAME,\nIFNULL( sum( a.financing_expenses ), 0 ) AS financing_expenses \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022 \nAND b.NAME IN ( '长虹能源', '同享科技' ) \nGROUP BY\nb.NAME \n) k \nORDER BY\nk.financing_expenses DESC \nLIMIT 1", 'order': False
    },
    {'query': '在所有已经退市的公司中，哪家公司的销售费用最高？', 'sql': 'SELECT\ncompany_name,\nIFNULL( sum( sales_fee ),0) AS sales_fee \nFROM\nincome_CN_STOCK_A t1\nINNER JOIN basic_info_CN_STOCK_A t2 ON t1.instrument = t2.instrument \nAND t2.delist_date IS NOT NULL \nGROUP BY\nt2.company_name \nORDER BY\nsales_fee DESC \nLIMIT 1', 'order': False
    },
    {'query': '在所有已经退市的公司中，哪家公司的销售费用最高？', 'sql': 'select k.company_name,sales_fee from (\nSELECT\nb.company_name,\nsum(a.sales_fee ) AS sales_fee \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nb.delist_date is not null\nGROUP BY\nb.name \n)k\nORDER BY\nk.sales_fee DESC \nLIMIT 1', 'order': False
    },
    {'query': '2022年的北京公司中，哪家公司的所得税费用最高？', 'sql': "SELECT\ncompany_name,\nsum( income_tax_cost ) AS income_tax_cost \nFROM\nincome_CN_STOCK_A t1\nINNER JOIN basic_info_CN_STOCK_A t2 ON t1.instrument = t2.instrument \nAND t2.company_province = '北京' \nWHERE\nYEAR ( report_date )= '2022' \nGROUP BY\nt2.company_name \nORDER BY\nincome_tax_cost DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年的北京公司中，哪家公司的所得税费用最高？', 'sql': "select k.company_name,income_tax_cost from (\nSELECT\nb.company_name,\nsum(a.income_tax_cost ) AS income_tax_cost \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nyear(a.report_date)=2022 and b.company_province = '北京'\nGROUP BY\nb.company_name \n)k\nORDER BY\nk.income_tax_cost DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年华夏银行的手续费及佣金收入和民生银行相比如何？', 'sql': "SELECT\nb.NAME,\nIFNULL( sum( a.fee_and_commi_income ), 0 ) AS fee_and_commi_income \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = '2022' \nAND b.NAME IN ( '华夏银行', '民生银行' ) \nGROUP BY\nb.NAME", 'order': False
    },
    {'query': '2022年华夏银行的手续费及佣金收入和民生银行相比如何？', 'sql': "SELECT \nNAME,\nsum(fee_and_commi_income) as fee_and_commi_income\nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = '2022' and b.name in('华夏银行', '民生银行')\nGROUP BY NAME ORDER BY fee_and_commi_income DESC", 'order': False
    },
    {'query': '2022年所有主板上市的公司中，哪家公司的营业总收入最高？', 'sql': "SELECT\nname,\noperating_total_revenue\nFROM\n(\nSELECT\nb.name,\nsum( a.operating_total_revenue ) AS operating_total_revenue \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022 \nAND b.list_board = '主板' \nGROUP BY\nb.name \n) k \nORDER BY\nk.operating_total_revenue DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年所有主板上市的公司中，哪家公司的营业总收入最高？', 'sql': "select k.company_name,operating_total_revenue from (\nSELECT\nb.company_name,\nsum(a.operating_total_revenue ) AS operating_total_revenue \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nyear(a.report_date)=2022 and b.list_board='主板' \nGROUP BY\nb.company_name \n)k\nORDER BY\nk.operating_total_revenue DESC \nLIMIT 1", 'order': False
    },
    {'query': '比较北证上的长虹能源和同享科技，哪家公司的资产减值损失更高？', 'sql': "SELECT\nname ,\nasset_impairment_loss,\nlist_board\nFROM\n(\nSELECT\nb.name,\nIFNULL(sum(a.asset_impairment_loss ),0) AS asset_impairment_loss ,list_board\nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022 \nAND b.name IN ( '长虹能源', '同享科技' ) \nAND b.list_board = '北证' \nGROUP BY\nb.name \n) k \nORDER BY\nk.asset_impairment_loss DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年在所有上海的公司中，哪家公司的管理费用最高？', 'sql': "SELECT\nname ,manage_fee\nFROM\n(\nSELECT\nb.name,\nIFNULL( sum( a.manage_fee ),0) AS manage_fee \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022\nAND b.company_province = '上海' \nGROUP BY\nb.name \n) k \nORDER BY\nk.manage_fee DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年在所有上海的公司中，哪家公司的管理费用最高？', 'sql': "select k.company_name,manage_fee from (\nSELECT\nb.company_name,\nsum(a.manage_fee ) AS manage_fee \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nyear(a.report_date)=2022 and b.company_province = '上海'\nGROUP BY\nb.company_name \n)k\nORDER BY\nk.manage_fee DESC \nLIMIT 1", 'order': False
    },
    {'query': '格力电器和比亚迪在2022年的基本每股收益中，哪家公司的收益更高？', 'sql': "SELECT\nname,\nbasic_eps\nFROM\nincome_CN_STOCK_A t1\nINNER JOIN basic_info_CN_STOCK_A t2 ON t1.instrument = t2.instrument \nAND t2.name IN ( '格力电器', '比亚迪' ) \nWHERE\nYEAR ( report_date )= '2022' \nGROUP BY\nname ,basic_eps\nORDER BY\nbasic_eps DESC \nLIMIT 1", 'order': False
    },
    {'query': '比较华夏银行和民生银行，哪家公司的财务费用更高？', 'sql': "SELECT\nk.name ,financing_expenses\nFROM\n(\nSELECT\nb.name,\nIFNULL( sum( a.financing_expenses ),0) AS financing_expenses \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nb.name IN ( '华夏银行', '民生银行' ) \nGROUP BY\nb.name \n) k \nORDER BY\nk.financing_expenses DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年所有四川的公司中，哪家公司的手续费及佣金支出最高？', 'sql': "select k.name,charge_and_commi_expenses from (\nSELECT\nb.name,\nIFNULL( sum(a.charge_and_commi_expenses ) ,0)AS charge_and_commi_expenses \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date ) = 2022 AND b.company_province = '四川省' \nGROUP BY\nb.name \n)k\nORDER BY\nk.charge_and_commi_expenses DESC \nLIMIT 1", 'order': False
    },
    {'query': '在所有已经退市的公司中，哪家公司的销售费用最高？', 'sql': 'SELECT\ncompany_name,\nIFNULL( sum( sales_fee ),0) AS sales_fee \nFROM\nincome_CN_STOCK_A t1\nINNER JOIN basic_info_CN_STOCK_A t2 ON t1.instrument = t2.instrument \nAND t2.delist_date IS NOT NULL \nGROUP BY\nt2.company_name \nORDER BY\nsales_fee DESC \nLIMIT 1', 'order': False
    },
    {'query': '在所有已经退市的公司中，哪家公司的销售费用最高？', 'sql': 'select k.company_name,sales_fee from (\nSELECT\nb.company_name,\nsum(a.sales_fee ) AS sales_fee \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nb.delist_date is not null\nGROUP BY\nb.name \n)k\nORDER BY\nk.sales_fee DESC \nLIMIT 1', 'order': False
    },
    {'query': '2022年的北京公司中，哪家公司的所得税费用最高？', 'sql': "SELECT\ncompany_name,\nsum( income_tax_cost ) AS income_tax_cost \nFROM\nincome_CN_STOCK_A t1\nINNER JOIN basic_info_CN_STOCK_A t2 ON t1.instrument = t2.instrument \nAND t2.company_province = '北京' \nWHERE\nYEAR ( report_date )= '2022' \nGROUP BY\nt2.company_name \nORDER BY\nincome_tax_cost DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年的北京公司中，哪家公司的所得税费用最高？', 'sql': "select k.company_name,income_tax_cost from (\nSELECT\nb.company_name,\nsum(a.income_tax_cost ) AS income_tax_cost \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nyear(a.report_date)=2022 and b.company_province = '北京'\nGROUP BY\nb.company_name \n)k\nORDER BY\nk.income_tax_cost DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年华夏银行的手续费及佣金收入和民生银行相比如何？', 'sql': "SELECT\nb.NAME,\nIFNULL( sum( a.fee_and_commi_income ), 0 ) AS fee_and_commi_income \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = '2022' \nAND b.NAME IN ( '华夏银行', '民生银行' ) \nGROUP BY\nb.NAME", 'order': False
    },
    {'query': '2022年华夏银行的手续费及佣金收入和民生银行相比如何？', 'sql': "SELECT \nNAME,\nsum(fee_and_commi_income) as fee_and_commi_income\nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = '2022' and b.name in('华夏银行', '民生银行')\nGROUP BY NAME ORDER BY fee_and_commi_income DESC", 'order': False
    },
    {'query': '2022年所有主板上市的公司中，哪家公司的营业总收入最高？', 'sql': "SELECT\nname,\noperating_total_revenue\nFROM\n(\nSELECT\nb.name,\nsum( a.operating_total_revenue ) AS operating_total_revenue \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022 \nAND b.list_board = '主板' \nGROUP BY\nb.name \n) k \nORDER BY\nk.operating_total_revenue DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年所有主板上市的公司中，哪家公司的营业总收入最高？', 'sql': "select k.company_name,operating_total_revenue from (\nSELECT\nb.company_name,\nsum(a.operating_total_revenue ) AS operating_total_revenue \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nyear(a.report_date)=2022 and b.list_board='主板' \nGROUP BY\nb.company_name \n)k\nORDER BY\nk.operating_total_revenue DESC \nLIMIT 1", 'order': False
    },
    {'query': '比较科创板上的长虹能源和同享科技，哪家公司的资产减值损失更高？', 'sql': "select k.name,asset_impairment_loss from (\nSELECT\nb.name,\nIFNULL( sum(a.asset_impairment_loss ),0) AS asset_impairment_loss \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nyear(a.report_date)=2022 and b.name IN ( '长虹能源', '同享科技' ) \nGROUP BY\nb.name \n)k\nORDER BY\nk.asset_impairment_loss DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年在所有上海的公司中，哪家公司的管理费用最高？', 'sql': "SELECT\nname ,manage_fee\nFROM\n(\nSELECT\nb.name,\nIFNULL( sum( a.manage_fee ),0) AS manage_fee \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022\nAND b.company_province = '上海' \nGROUP BY\nb.name \n) k \nORDER BY\nk.manage_fee DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年在所有上海的公司中，哪家公司的管理费用最高？', 'sql': "select k.company_name,manage_fee from (\nSELECT\nb.company_name,\nsum(a.manage_fee ) AS manage_fee \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nyear(a.report_date)=2022 and b.company_province = '上海'\nGROUP BY\nb.company_name \n)k\nORDER BY\nk.manage_fee DESC \nLIMIT 1", 'order': False
    },
    {'query': '格力电器和华夏银行在2022年的基本每股收益中，哪家公司的收益更高？', 'sql': "SELECT\nname,\nbasic_eps\nFROM\nincome_CN_STOCK_A t1\nINNER JOIN basic_info_CN_STOCK_A t2 ON t1.instrument = t2.instrument \nAND t2.name IN ( '格力电器', '华夏银行' ) \nWHERE\nYEAR ( report_date )= '2022' \nGROUP BY\nname ,basic_eps\nORDER BY\nbasic_eps DESC \nLIMIT 1", 'order': False
    },
    {'query': '请列出2022年应付债券占总负债比例最高的五家公司？', 'sql': 'SELECT \nname,\n(a.bond_payable / a.total_liab) AS ratio\nFROM \nbalance_sheet_CN_STOCK_A a JOIN basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE \nYEAR(a.report_date) = 2022\nGROUP BY\nb.name\nORDER BY \nratio DESC\nLIMIT 5;', 'order': True
    },
    {'query': '能否找出2022年连续三个季度应收利息占总资产的比例下降的上市公司？', 'sql': 'SELECT DISTINCT a.instrument, a.company_name\nFROM (\nSELECT\nbs.instrument,\nbs.fs_quarter_index,\nbs.interest_receivable / bs.total_assets AS interest_to_assets_ratio,\nLAG(bs.interest_receivable / bs.total_assets,1) OVER (PARTITION BY bs.instrument ORDER BY bs.fs_quarter_index) AS prev_interest_to_assets_ratio,\nLAG(bs.interest_receivable / bs.total_assets,2) OVER (PARTITION BY bs.instrument ORDER BY bs.fs_quarter_index) AS prev_prev_interest_to_assets_ratio\nFROM balance_sheet_CN_STOCK_A bs\nWHERE bs.total_assets > 0 and YEAR(bs.report_date) = 2022\n) AS derived\nJOIN basic_info_CN_STOCK_A a ON derived.instrument = a.instrument\nWHERE\nderived.interest_to_assets_ratio < derived.prev_interest_to_assets_ratio\nAND derived.prev_interest_to_assets_ratio < derived.prev_prev_interest_to_assets_ratio;', 'order': False
    },
    {'query': '请问2022第四季度相比于2021第一季度，上港集团的应付账款有何变化？', 'sql': "SELECT NAME\n,\nSUM(t2.accounts_payable) - SUM(t3.accounts_payable )\nFROM\nbasic_info_CN_STOCK_A t1\nINNER JOIN balance_sheet_CN_STOCK_A t2 ON t1.instrument = t2.instrument \nAND YEAR ( t2.report_date ) = 2022 \nAND t2.fs_quarter_index = 1 \nAND t1.NAME = '上港集团'\nINNER JOIN balance_sheet_CN_STOCK_A t3 ON t1.instrument = t3.instrument \nAND YEAR ( t3.report_date ) = 2021 \nAND t3.fs_quarter_index = 4 \nAND t1.NAME = '上港集团'", 'order': False
    },
    {'query': '2023年哪些公司的预计负债同比增长最快？', 'sql': 'SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as yoy\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.estimated_liab) as val\nFROM balance_sheet_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2023 GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.estimated_liab) as val\nFROM balance_sheet_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2022 GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY yoy DESC LIMIT 1', 'order': False
    },
    {'query': '请问2023年一年内到期的非流动资产占总资产的比例最高的是哪些公司？', 'sql': "SELECT\nname,\nconcat( round( SUM(noncurrent_asset_due_within1y) / SUM(total_assets) * 100, 2 ), '%' ) AS rate \nFROM\nbasic_info_CN_STOCK_A a\nINNER JOIN balance_sheet_CN_STOCK_A b ON a.instrument = b.instrument \nAND YEAR ( b.report_date ) = 2023\nGROUP BY name\nORDER BY\nrate DESC \nLIMIT 5", 'order': True
    },
    {'query': '2022年哪些公司的一年内到期的非流动负债增长最快？', 'sql': "SELECT \nb2022.instrument,\nb2022.company_name,\nb2022.val as val_2022,\nb2021.val as val_2021,\n(b2022.val - b2021.val) AS growth\nFROM\n(SELECT \nbs.instrument,\nbi.company_name,\nSUM( bs.noncurrent_liab_due_in1y) as val\nFROM \nbalance_sheet_CN_STOCK_A bs\nJOIN \nbasic_info_CN_STOCK_A bi ON bs.instrument = bi.instrument\nWHERE \nYEAR(bs.report_date) = '2022'\nGROUP BY \nbs.instrument,\nbi.company_name) b2022\nJOIN\n(SELECT \nbs.instrument,\nbi.company_name,\nSUM( bs.noncurrent_liab_due_in1y) as val\nFROM \nbalance_sheet_CN_STOCK_A bs\nJOIN \nbasic_info_CN_STOCK_A bi ON bs.instrument = bi.instrument\nWHERE \nYEAR(bs.report_date) = '2021'\nGROUP BY \nbs.instrument,\nbi.company_name) b2021 ON b2022.instrument = b2021.instrument\nORDER BY \ngrowth DESC LIMIT 5;", 'order': True
    },
    {'query': '2023年第一季度哪个公司的预收款项环比增长最快？', 'sql': 'SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as mom\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.advance_payment) as val\nFROM balance_sheet_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2023 and a.fs_quarter_index = 1 GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.advance_payment) as val\nFROM balance_sheet_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2022 and a.fs_quarter_index = 1 GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY mom DESC LIMIT 1', 'order': False
    },
    {'query': '2023年哪个公司的实收资本占总资产的比例最高？', 'sql': "SELECT\nname , rate\nFROM\n(\nSELECT\na.name,\nconcat( round( SUM(b.actual_received_capital) / SUM(b.total_assets) * 100, 2 ), '%' ) AS rate \nFROM\nbasic_info_CN_STOCK_A a\nINNER JOIN balance_sheet_CN_STOCK_A b ON a.instrument = b.instrument \nAND YEAR ( b.report_date ) = 2023 \nGROUP BY a.name\n) k \nORDER BY\nk.rate DESC \nLIMIT 1", 'order': False
    },
    {'query': '2022年华夏银行和民生银行哪家公司的所有者权益合计更高？', 'sql': "SELECT\nCASE\n\nWHEN\nk.hx_total_owner_equity > k.ms_total_owner_equity THEN\n'华夏银行' \nWHEN k.hx_total_owner_equity = k.ms_total_owner_equity THEN\n'一样高' ELSE '民生银行' \nEND \nFROM\n(\nSELECT\nsum( CASE WHEN b.name = '华夏银行' THEN a.total_owner_equity ELSE 0 END ) AS hx_total_owner_equity,\nsum( CASE WHEN b.name = '民生银行' THEN a.total_owner_equity ELSE 0 END ) AS ms_total_owner_equity \nFROM\nbalance_sheet_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022 \n) k", 'order': False
    },
    {'query': '2022年华夏银行和民生银行哪家公司的所有者权益合计更高？', 'sql': "SELECT\nCASE\n\nWHEN\nk.hx_total_owner_equity > k.ms_total_owner_equity THEN\n'华夏银行' \nWHEN k.hx_total_owner_equity = k.ms_total_owner_equity THEN\n'一样高' ELSE '民生银行' \nEND \nFROM\n(\nSELECT\nsum( CASE WHEN b.name = '华夏银行' THEN a.total_owner_equity ELSE 0 END ) AS hx_total_owner_equity,\nsum( CASE WHEN b.name = '民生银行' THEN a.total_owner_equity ELSE 0 END ) AS ms_total_owner_equity \nFROM\nbalance_sheet_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = '2022' \n) k", 'order': False
    },
    {'query': '过去五年中，哪家公司的收到的预付款项与付出的预付款项比率波动最剧烈？', 'sql': 'SELECT\nbi.company_name,\nSTDDEV( ratio ) AS ratio_stddev \nFROM\n(\nSELECT\nbs.instrument,\n( CASE WHEN sum( bs.prepays ) = 0 THEN NULL ELSE SUM( bs.advance_payment ) / sum( bs.prepays ) END ) AS ratio \nFROM\nbalance_sheet_CN_STOCK_A bs \nWHERE\nbs.report_date >= DATE_SUB( CURDATE(), INTERVAL 5 YEAR ) \nGROUP BY\nbs.instrument \n) AS ratios\nJOIN basic_info_CN_STOCK_A bi ON ratios.instrument = bi.instrument \nGROUP BY\nbi.company_name \nHAVING\nratio_stddev IS NOT NULL \nORDER BY\nratio_stddev DESC \nLIMIT 1;', 'order': False
    },
    {'query': '2023年第2季度哪些公司的应付手续费及佣金环比增长最快？', 'sql': 'SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as mom\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.charge_and_commi_payable) as val\nFROM balance_sheet_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2023 and a.fs_quarter_index = 1 GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.charge_and_commi_payable) as val\nFROM balance_sheet_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2022 and a.fs_quarter_index = 4 GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY mom DESC LIMIT 1', 'order': False
    },
    {'query': '2023年上汽集团的研发费用在其总成本中占比多少？', 'sql': "SELECT\nconcat( round( sum( a.rad_cost_sum ) / sum( a.operating_total_cost ) * 100, 2 ), '%' ) AS rate \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nb.name IN ( '上汽集团' ) and YEAR (a.report_date ) = 2023", 'order': False
    },
    {'query': '同享科技2023年归属于母公司所有者的净利润年增长率（YoY）是多少？', 'sql': "SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as yoy\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.np_atoopc) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2023 and b.NAME = '同享科技' GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.np_atoopc) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2022 and b.NAME = '同享科技' GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY yoy DESC LIMIT 1", 'order': False
    },
    {'query': '请问2023年全年，广东省市场的营业收入占全国总营业收入的比例为何？', 'sql': "SELECT\nSUM(CASE WHEN b.company_province = '广东省' THEN i.revenue ELSE 0 END) / SUM(i.revenue) AS Guangdong_Province_Revenue_Ratio\nFROM\nincome_CN_STOCK_A AS i\nINNER JOIN\nbasic_info_CN_STOCK_A AS b\nON\ni.instrument = b.instrument\nWHERE\ni.report_date BETWEEN '2023-01-01' AND '2023-12-31';", 'order': False
    },
    {'query': '格力电器的手续费及佣金支出在其总支出中占比多少？', 'sql': "SELECT \nb.company_name,\ni.instrument,\nYEAR(i.report_date),\nSUM(i.charge_and_commi_expenses) as charge_and_commi_expenses,\nSUM(i.operating_total_cost) as operating_total_cost,\n( SUM(i.charge_and_commi_expenses) / SUM(i.operating_total_cost)) * 100 AS commi_expense_percentage\nFROM \nbasic_info_CN_STOCK_A b\nJOIN \nincome_CN_STOCK_A i ON b.instrument = i.instrument\nWHERE \nb.name = '格力电器'\nGROUP BY \nb.company_name,\ni.instrument,\nYEAR(i.report_date)\nORDER BY \nYEAR(i.report_date) DESC", 'order': True
    },
    {'query': '请问2022年第3季度，宝钢股份的营业收入环比增长率是多少？', 'sql': "SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as mom\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.revenue) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2022 and a.fs_quarter_index = 3 and b.`name` = '宝钢股份' GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.revenue) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2022 and a.fs_quarter_index = 2 and b.`name` = '宝钢股份' GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY mom DESC LIMIT 1", 'order': False
    },
    {'query': '请问过去五年中，中国石化的年度总利润同比增长率是多少？', 'sql': "SELECT \nA.year,\nSUM(A.np_atoopc) AS net_profit,\n(SUM(A.np_atoopc) / LAG(SUM(A.np_atoopc)) OVER (ORDER BY A.year) - 1) AS growth_rate\nFROM (\nSELECT \nYEAR(income.report_date) AS year,\nSUM(income.np_atoopc) as np_atoopc\nFROM \nincome_CN_STOCK_A AS income\nJOIN \nbasic_info_CN_STOCK_A AS info ON income.instrument = info.instrument\nWHERE \ninfo.name = '中国石化' AND\nincome.report_date IS NOT NULL AND \nYEAR(income.report_date) BETWEEN YEAR(CURDATE()) - 5 AND YEAR(CURDATE()) - 1\nGROUP BY \nYEAR(income.report_date)\n) AS A\nGROUP BY\nA.year\nORDER BY \nA.year;", 'order': True
    },
    {'query': '2022年第二季度与20221年同期相比，民生银行的财务费用同比增长率是多少？', 'sql': "SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as yoy\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.total_profit) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2022 and b.NAME = '中国石化' AND fs_quarter_index = 2 GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.total_profit) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2021 and b.NAME = '中国石化' AND fs_quarter_index = 2 GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY yoy DESC LIMIT 1", 'order': False
    },
    {'query': '2023第一季度上港集团的营业总收入环比增长率是多少？', 'sql': "SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as mom\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.revenue) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE a.report_date BETWEEN '2023-01-01' and '2023-03-31' and b.`name` = '上汽集团' GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.revenue) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE a.report_date BETWEEN '2022-10-01' and '2022-12-31' and b.`name` = '上汽集团' GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY mom DESC LIMIT 1", 'order': False
    },
    {'query': '2023年第一季度，华夏银行的基本每股收益同比增长率是多少？', 'sql': "SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as yoy\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.basic_eps) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2022 and b.NAME = '华夏银行' AND fs_quarter_index = 1 GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.basic_eps) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2021 and b.NAME = '华夏银行' AND fs_quarter_index = 1 GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY yoy DESC LIMIT 1", 'order': False
    },
    {'query': '2022年，民生银行的投资收益率（Investment Income Ratio）如何？', 'sql': "SELECT\nconcat( round( sum( a.invest_income ) / sum( a.revenue ) * 100, 2 ), '%' ) AS rate \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nb.name IN ( '民生银行' ) and YEAR (a.report_date ) = '2022'", 'order': False
    },
    {'query': '请问2021年第二季度，上港集团的营业成本环比增长率是多少？', 'sql': "SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as mom\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.operating_cost) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2021 and a.fs_quarter_index = 2 and b.`name` = '上汽集团' GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.operating_cost) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2021 and a.fs_quarter_index = 1 and b.`name` = '上汽集团' GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY mom DESC LIMIT 1", 'order': False
    },
    {'query': '请问2023年全年，宝钢股份的销售费用在营业总成本中占比是多少？', 'sql': "SELECT\nconcat( round( sum( a.sales_fee ) / sum( a.operating_cost ) * 100, 2 ), '%' ) AS rate \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nb.name IN ( '宝钢股份' ) and YEAR (a.report_date ) = 2023", 'order': False
    },
    {'query': '去年第一季度，中国石化的税金及附加在营业总成本中的占比是多少？', 'sql': "SELECT\nb.name,\nconcat( round( operating_taxes_and_surcharge / operating_total_cost * 100, 2 ), '%' ) \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nAND b.name = '中国石化' \nWHERE\nYEAR ( report_date ) = YEAR ( CURRENT_DATE ) -1\nAND fs_quarter_index = 1;", 'order': False
    },
    {'query': '2023年第一季度与上一季度相比，格力电器的营业总收入环比增长率是多少？', 'sql': "SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as mom\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.operating_total_revenue) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2023 and a.fs_quarter_index = 1 and b.`name` = '格力电器' GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.operating_total_revenue) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2022 and a.fs_quarter_index = 4 and b.`name` = '格力电器' GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY mom DESC LIMIT 1", 'order': False
    },
    {'query': '2023年第一季度，五粮液的现金流量套期储备在营业总收入中的占比是多少？', 'sql': "SELECT\nconcat( round( IFNULL(sum( a.cash_flow_hedge_reserve ),0) / IFNULL(sum( a.operating_total_revenue ),0) * 100, 2 ), '%' ) AS rate \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nb.name IN ( '五粮液' ) and a.fs_quarter_index = 1 and year(a.report_date) = 2023;", 'order': False
    },
    {'query': '去年2月份哪个公司的净利润环比增长最多？', 'sql': "SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as mom\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.np_cfs) as val\nFROM cash_flow_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE a.date BETWEEN '2022-02-01' and '2022-2-28' GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.net_increase_in_cce) as val\nFROM cash_flow_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE a.date BETWEEN '2022-01-01' and '2022-1-31' GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY mom DESC LIMIT 1", 'order': False
    },
    {'query': '2023年公司的投资活动现金流出排名前五的企业？', 'sql': "SELECT\nb.company_name,\nSUM(sub_total_of_cos_from_ia) AS total_investment_outflow\nFROM\ncash_flow_CN_STOCK_A c\nJOIN\nbasic_info_CN_STOCK_A b ON c.instrument = b.instrument\nWHERE\nc.report_date BETWEEN '2023-01-01' AND '2023-12-31'\nGROUP BY\nb.company_name\nORDER BY\ntotal_investment_outflow DESC\nLIMIT 5;", 'order': True
    },
    {'query': '2022年，哪个公司的现金及现金等价物净增加额同比增长最高？', 'sql': 'SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as yoy\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.net_increase_in_cce) as val\nFROM cash_flow_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2022 GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.net_increase_in_cce) as val\nFROM cash_flow_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2021 GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY yoy DESC LIMIT 1', 'order': False
    },
    {'query': '请问在2022年上半年，哪些公司的经营活动现金流量净额超过了1000万元？', 'sql': "SELECT\na.name \nFROM\nbasic_info_CN_STOCK_A a\nINNER JOIN cash_flow_CN_STOCK_A b ON a.instrument = b.instrument \nAND YEAR ( b.report_date ) = '2022' \nAND b.fs_quarter_index IN ( 1, 2 ) \nAND a.delist_date IS NULL\nGROUP BY\na.name \nHAVING\nsum( sub_total_of_ci_from_oa ) - sum( sub_total_of_cos_from_oa ) > 10000000", 'order': False
    },
    {'query': '在2023年第一季度公司的投资活动现金流入小计超过其经营活动现金流入小计的公司数量是多少？', 'sql': "SELECT COUNT(DISTINCT c.instrument)\nFROM cash_flow_CN_STOCK_A c\nWHERE c.report_date BETWEEN '2023-01-01' AND '2023-03-31'\nAND c.sub_total_of_ci_from_ia > c.sub_total_of_ci_from_oa;", 'order': False
    },
    {'query': '请问2023年全年，比亚迪的营业外支出在营业总成本中的占比是多少？', 'sql': "SELECT\nconcat( round( sum( a.nonoperating_cost ) / sum( a.operating_total_cost ) * 100, 2 ), '%' ) AS rate \nFROM\nincome_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nb.name IN ( '比亚迪' ) and year(a.report_date ) = 2023", 'order': False
    },
    {'query': '2022第一季度，长虹能源的营业外收入环比增长率是多少？', 'sql': "SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as mom\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.non_operating_income) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2022 and a.fs_quarter_index = 1 and b.`name` = '长虹能源' GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.non_operating_income) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2021 and a.fs_quarter_index = 4 and b.`name` = '长虹能源' GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY mom DESC LIMIT 1", 'order': False
    },
    {'query': '2023年第一季度与去年同期相比，同享科技的财务费用同比增长率是多少？', 'sql': "SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as yoy\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.financing_expenses) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2023 and b.NAME = '同享科技' AND fs_quarter_index = 1 GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.financing_expenses) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2022 and b.NAME = '同享科技' AND fs_quarter_index = 1 GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY yoy DESC LIMIT 1", 'order': False
    },
    {'query': '2022年，哪个公司的财务费用同比增长最高？', 'sql': 'SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as yoy\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.financing_expenses) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2022 AND fs_quarter_index = 1 GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.financing_expenses) as val\nFROM income_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2021 AND fs_quarter_index = 1 GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY yoy DESC LIMIT 1', 'order': False
    },
    {'query': '2023年第二季度，哪个公司的投资活动现金流入占其总现金流入的比例最高？', 'sql': 'SELECT \nb.company_name,\n(SUM(i.sub_total_of_ci_from_ia) / SUM(i.sub_total_of_ci_from_oa + i.sub_total_of_ci_from_ia + i.sub_total_of_ci_from_fa)) * 100 AS InvestmentCashInflowPercentage\nFROM \ncash_flow_CN_STOCK_A AS i\nJOIN \nbasic_info_CN_STOCK_A AS b\nON \ni.instrument = b.instrument\nWHERE \ni.fs_quarter_index = 2\nGROUP BY \nb.company_name\nORDER BY \nInvestmentCashInflowPercentage DESC\nLIMIT 1;', 'order': False
    },
    {'query': '请问在2022~2023两年中，哪个公司的经营活动现金流量净额占其总资产的比例最高？', 'sql': 'SELECT\nbi.company_name,\ncf.instrument,\n(SUM(cf.ncf_from_oa) / SUM(bs.total_assets)) AS max_cash_flow_to_assets_ratio\nFROM\ncash_flow_CN_STOCK_A AS cf\nJOIN\nbasic_info_CN_STOCK_A AS bi\nON\ncf.instrument = bi.instrument\nJOIN\nbalance_sheet_CN_STOCK_A AS bs\nON\ncf.instrument = bs.instrument\nWHERE\nYEAR(cf.report_date) IN (2023,2022)\nGROUP BY\ncf.instrument\nORDER BY\nmax_cash_flow_to_assets_ratio DESC\nLIMIT 1;\n', 'order': False
    },
    {'query': '2021年2季度，哪个公司的现金及现金等价物净增加额环比增长最快？', 'sql': 'SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as qoq\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.net_increase_in_cce) as val\nFROM cash_flow_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2021 AND fs_quarter_index = 2 GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.net_increase_in_cce) as val\nFROM cash_flow_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2021 AND fs_quarter_index = 1 GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY qoq DESC LIMIT 1', 'order': False
    },
    {'query': '2021年哪个公司的财务费用同比增长率最高？', 'sql': 'SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as yoy\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.finance_cost_cfs) as val\nFROM cash_flow_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2021 GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.finance_cost_cfs) as val\nFROM cash_flow_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2020 GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY yoy DESC LIMIT 1', 'order': False
    },
    {'query': '2022年各季度，各个行业的现金流量分布情况如何？', 'sql': "SELECT\nb.company_name,\ncf.instrument,\ncf.fs_quarter_index AS quarter,\nSUM(cf.ncf_from_oa) AS operating_activities_cash_flow,\nSUM(cf.ncf_from_ia) AS investing_activities_cash_flow,\nSUM(cf.ncf_from_fa) AS financing_activities_cash_flow,\n(SUM(cf.ncf_from_oa) + SUM(cf.ncf_from_ia) + SUM(cf.ncf_from_fa)) AS cash_flow_performance\nFROM\ncash_flow_CN_STOCK_A cf\nJOIN\nbasic_info_CN_STOCK_A b ON cf.instrument = b.instrument\nWHERE\ncf.report_date >= '2022-01-01' AND\ncf.report_date <= '2022-12-31'\nGROUP BY\nb.company_name,\ncf.instrument,\ncf.fs_quarter_index;", 'order': False
    },
    {'query': '2023年哪家公司的现金流量表中的经营现金流净额对净利润的比率最高？', 'sql': 'SELECT b.company_name, \n(SUM(c.ncf_from_oa) / SUM(c.np_cfs)) AS ratio\nFROM cash_flow_CN_STOCK_A AS c\nJOIN basic_info_CN_STOCK_A AS b ON c.instrument = b.instrument\nWHERE YEAR(c.report_date) = 2023\nGROUP BY b.company_name\nORDER BY ratio DESC\nLIMIT 1;', 'order': False
    },
    {'query': '2022年同享科技的工资税负比率是多少？', 'sql': "SELECT\nconcat( round( sum( a.payroll_payable + a.tax_payable ) / SUM( operating_total_revenue ) * 100, 2 ), '%' ) AS 工资税负比率 \nFROM\nbalance_sheet_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument\nINNER JOIN income_CN_STOCK_A c ON b.instrument = c.instrument \nWHERE\nb.NAME IN ( '同享科技' ) \nAND YEAR ( a.report_date ) = 2022;", 'order': False
    },
    {'query': '2022年中国石化的固定资产和投资性房地产占总资产的比例是多少？', 'sql': "SELECT\nconcat( round( IFNULL(sum( a.fixed_asset ),0) / sum( a.total_assets ) * 100, 2 ), '%' ) AS fixed_asset_rate ,\nconcat( round( IFNULL(sum( a.invest_property ),0) / sum( a.total_assets ) * 100, 2 ), '%' ) AS invest_property_rate \nFROM\nbalance_sheet_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nb.name IN ( '中国石化' ) AND\nYEAR (a.report_date ) = 2022;", 'order': False
    },
    {'query': '2022年长虹能源的应付债券和应付短期债券的分别是多少？', 'sql': "SELECT\nSUM( bond_payable ),\nSUM( st_bond_payable ) \nFROM\nbalance_sheet_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nb.NAME IN ( '上汽集团' ) \nAND YEAR ( a.report_date ) = 2022;", 'order': False
    },
    {'query': '2022年宝钢股份的流动资产和非流动资产哪个更高？', 'sql': "SELECT\nCASE\nWHEN\nsum( a.total_current_assets ) >= sum( a.total_noncurrent_assets ) THEN\n'流动资产合计高' \nwhen sum( a.total_current_assets ) = sum( a.total_noncurrent_assets ) THEN\n'一样高' \nELSE '非流动资产合计高' \nEND \nFROM\nbalance_sheet_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( report_date ) = 2022 AND b.name = '宝钢股份'", 'order': False
    },
    {'query': '2022年上港集团和比亚迪哪家公司的未分配利润更高？', 'sql': "SELECT\nCASE\nWHEN\nk.sg_undstrbtd_profit > k.byd_undstrbtd_profit THEN\n'上港集团未分配利润高' \nWHEN k.sg_undstrbtd_profit = k.byd_undstrbtd_profit THEN\n'一样高' ELSE '比亚迪未分配利润高' \nEND \nFROM\n(\nSELECT\nsum( CASE WHEN b.name = '上港集团' THEN a.undstrbtd_profit ELSE 0 END ) AS sg_undstrbtd_profit,\nsum( CASE WHEN b.name = '比亚迪' THEN a.undstrbtd_profit ELSE 0 END ) AS byd_undstrbtd_profit \nFROM\nbalance_sheet_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR (a.report_date ) = 2022 \n) k", 'order': False
    },
    {'query': '2022年华夏银行和民生银行哪家公司的所有者权益合计更高？', 'sql': "SELECT\nCASE\n\nWHEN\nk.hx_total_owner_equity > k.ms_total_owner_equity THEN\n'华夏银行' \nWHEN k.hx_total_owner_equity = k.ms_total_owner_equity THEN\n'一样高' ELSE '民生银行' \nEND \nFROM\n(\nSELECT\nsum( CASE WHEN b.name = '华夏银行' THEN a.total_owner_equity ELSE 0 END ) AS hx_total_owner_equity,\nsum( CASE WHEN b.name = '民生银行' THEN a.total_owner_equity ELSE 0 END ) AS ms_total_owner_equity \nFROM\nbalance_sheet_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = 2022 \n) k", 'order': False
    },
    {'query': '2022年华夏银行和民生银行哪家公司的所有者权益合计更高？', 'sql': "SELECT\nCASE\n\nWHEN\nk.hx_total_owner_equity > k.ms_total_owner_equity THEN\n'华夏银行' \nWHEN k.hx_total_owner_equity = k.ms_total_owner_equity THEN\n'一样高' ELSE '民生银行' \nEND \nFROM\n(\nSELECT\nsum( CASE WHEN b.name = '华夏银行' THEN a.total_owner_equity ELSE 0 END ) AS hx_total_owner_equity,\nsum( CASE WHEN b.name = '民生银行' THEN a.total_owner_equity ELSE 0 END ) AS ms_total_owner_equity \nFROM\nbalance_sheet_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = '2022' \n) k", 'order': False
    },
    {'query': '在2023年，北京哪个公司的负债和所有者权益总计同比增长最快？', 'sql': "SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as yoy\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.total_liab_and_owner_equity) as val\nFROM balance_sheet_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE b.company_province = '北京' and YEAR(a.report_date) = 2023 GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.total_liab_and_owner_equity) as val\nFROM balance_sheet_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE b.company_province = '北京' and YEAR(a.report_date) = 2022 GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY yoy DESC LIMIT 1", 'order': False
    },
    {'query': '2023年格力电器的现金及现金等价物比率如何？', 'sql': "SELECT\nconcat( round( sum( a.currency_fund + a.tradable_fnncl_assets) / sum( a.total_assets ) * 100, 2 ), '%' ) AS rate \nFROM\nbalance_sheet_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nb.name IN ( '格力电器' ) and YEAR (a.report_date ) = '2022'", 'order': False
    },
    {'query': '请列出2022年股东权益比率（Equity Ratio）最高的五家上市公司？', 'sql': "SELECT \nNAME,\nconcat( round( SUM( total_owner_equity ) / SUM( total_assets ) * 100, 2 ), '%' ) AS ratio \nFROM\nbasic_info_CN_STOCK_A t1\nINNER JOIN balance_sheet_CN_STOCK_A t2 ON t1.instrument = t2.instrument \nAND YEAR ( t2.report_date )= '2022' \nGROUP BY\nNAME \nORDER BY\nratio DESC \nLIMIT 5", 'order': True
    },
    {'query': '在2023年，哪个公司的应付股利占总负债的比例最高？', 'sql': "SELECT \nname ,rate\nFROM \n(\nSELECT \nb.name,\nconcat( round( sum( a.dividend_payable ) / sum( a.total_liab ) * 100, 2 ), '%' ) AS rate \nFROM\nbalance_sheet_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = '2023' \nGROUP BY\nb.name \n) k \nORDER BY\nk.rate DESC \nLIMIT 1", 'order': False
    },
    {'query': '请列出2022年利息收入比率（Interest Income Ratio）最高的五家上市公司。', 'sql': "SELECT\nname ,rate\nFROM\n(\nSELECT\nb.name,\nconcat( round( sum( a.interest_receivable ) / sum( a.total_assets ) * 100, 2 ), '%' ) AS rate \nFROM\nbalance_sheet_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = '2022' \nGROUP BY\nb.name \n) k \nORDER BY\nk.rate DESC \nLIMIT 5", 'order': True
    },
    {'query': '过去五年中，哪家公司的预收款项与应付账款比率最高？', 'sql': "SELECT\nname , rate\nFROM\n(\nSELECT\nb.name,\nconcat( round( sum( a.advance_payment ) / sum( a.accounts_payable ) * 100, 2 ), '%' ) AS rate \nFROM\nbalance_sheet_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nreport_date >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)\nGROUP BY\nb.name \n) k \nORDER BY\nk.rate DESC \nLIMIT 1;", 'order': False
    },
    {'query': '在2023年3月，负债环比增长率最高的公司是？', 'sql': "SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as mom\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.total_liab) as val\nFROM balance_sheet_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE a.report_date BETWEEN '2023-01-01' and '2023-03-31' GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.total_liab) as val\nFROM balance_sheet_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE a.report_date BETWEEN '2022-01-01' and '2022-03-31' GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY mom DESC LIMIT 1\n", 'order': False
    },
    {'query': '请列出2022年应付手续费及佣金占总负债比例最高的五家公司？', 'sql': "SELECT\nname ,rate\nFROM\n(\nSELECT\nb.name,\nconcat( round( sum( a.charge_and_commi_payable ) / sum( a.total_liab ) * 100, 2 ), '%' ) AS rate \nFROM\nbalance_sheet_CN_STOCK_A a\nINNER JOIN basic_info_CN_STOCK_A b ON a.instrument = b.instrument \nWHERE\nYEAR ( a.report_date ) = '2022' \nGROUP BY\nb.name \n) k \nORDER BY\nk.rate DESC \nLIMIT 5", 'order': True
    },
    {'query': '2022年递延所得税资产同比增长率前5的是哪几家公司？', 'sql': 'SELECT\nt1.name,\n(t1.val - t2.val) / t2.val as yoy\nFROM\n(SELECT \nb.name,\nb.instrument,\nsum(a.dt_assets) as val\nFROM balance_sheet_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2022 GROUP BY b.name,\nb.instrument) t1 LEFT JOIN (SELECT \nb.name,\nb.instrument,\nsum(a.dt_assets) as val\nFROM balance_sheet_CN_STOCK_A a join basic_info_CN_STOCK_A b on b.instrument = a.instrument\nWHERE YEAR(a.report_date) = 2021 GROUP BY b.name,\nb.instrument) t2 on t1.instrument = t2.instrument\nORDER BY yoy DESC LIMIT 5', 'order': True
    }
]
train_data = all_data[0:100]
test_data = all_data[100:110]
db_type = 'mysql'
table_info = '''数据库的包含的表名有:['balance_sheet_CN_STOCK_A', 'basic_info_CN_STOCK_A', 'cash_flow_CN_STOCK_A', 'income_CN_STOCK_A']

CREATE TABLE `balance_sheet_CN_STOCK_A` (
	date DATE NOT NULL COMMENT '公告日', 
	instrument VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '股票代码', 
	report_date DATE NOT NULL COMMENT '报告期', 
	change_type INTEGER COMMENT '调整类型 0：未调整，1：调整过', 
	fs_quarter_index INTEGER COMMENT '对应季度', 
	account_receivable DOUBLE COMMENT '应收账款', 
	accounts_payable DOUBLE COMMENT '应付账款', 
	act_underwriting_sec DOUBLE COMMENT '代理承销证券款', 
	acting_td_sec DOUBLE COMMENT '代理买卖证券款', 
	actual_received_capital DOUBLE COMMENT '实收资本（或股本）', 
	advance_payment DOUBLE COMMENT '预收款项', 
	appropriative_reserve DOUBLE COMMENT '专项储备', 
	asset_diff_sri DOUBLE COMMENT '资产差额（特殊报表科目）', 
	asset_diff_tbi DOUBLE COMMENT '资产差额（合计平衡科目）', 
	bill_and_account_payable DOUBLE COMMENT '应付票据及应付账款', 
	bill_and_account_receivable DOUBLE COMMENT '应收票据及应收账款', 
	bill_payable DOUBLE COMMENT '应付票据', 
	bill_receivable DOUBLE COMMENT '应收票据', 
	bond_payable DOUBLE COMMENT '应付债券', 
	borrowing_funds DOUBLE COMMENT '拆入资金', 
	bs_other_compre_income DOUBLE COMMENT '其他综合收益', 
	buy_resale_fnncl_assets DOUBLE COMMENT '买入返售金融资产', 
	capital_reserve DOUBLE COMMENT '资本公积', 
	charge_and_commi_payable DOUBLE COMMENT '应付手续费及佣金', 
	construction_in_process DOUBLE COMMENT '在建工程', 
	construction_in_process_sum DOUBLE COMMENT '在建工程合计', 
	contract_asset DOUBLE COMMENT '合同资产', 
	contract_liab DOUBLE COMMENT '合同负债', 
	currency_fund DOUBLE COMMENT '货币资金', 
	debt_right_invest DOUBLE COMMENT '债权投资', 
	derivative_fnncl_assets DOUBLE COMMENT '衍生金融资产', 
	derivative_fnncl_liab DOUBLE COMMENT '衍生金融负债', 
	dev_expenditure DOUBLE COMMENT '开发支出', 
	differed_income_current_liab DOUBLE COMMENT '递延收益-流动负债', 
	differed_incomencl DOUBLE COMMENT '递延收益-非流动负债', 
	divided_into_asset_for_sale DOUBLE COMMENT '持有待售资产', 
	divided_into_liab_for_sale DOUBLE COMMENT '持有待售负债', 
	dividend_payable DOUBLE COMMENT '应付股利', 
	dividend_receivable DOUBLE COMMENT '应收股利', 
	dt_assets DOUBLE COMMENT '递延所得税资产', 
	dt_liab DOUBLE COMMENT '递延所得税负债', 
	earned_surplus DOUBLE COMMENT '盈余公积', 
	equity_right_diff_tbi DOUBLE COMMENT '股权权益差额（合计平衡科目）', 
	estimated_liab DOUBLE COMMENT '预计负债', 
	fa_calc_by_amortized_cost DOUBLE COMMENT '以摊余成本计量的金融资产', 
	fixed_asset DOUBLE COMMENT '固定资产', 
	fixed_asset_sum DOUBLE COMMENT '固定资产合计', 
	fixed_assets_disposal DOUBLE COMMENT '固定资产清理', 
	flow_assets_diff_sri DOUBLE COMMENT '流动资产差额（特殊报表科目）', 
	flow_assets_diff_tbi DOUBLE COMMENT '流动资产差额（合计平衡科目）', 
	flow_debt_diff_sri DOUBLE COMMENT '流动负债差额（特殊报表科目）', 
	flow_debt_diff_tbi DOUBLE COMMENT '流动负债差额（合计平衡科目）', 
	fnncl_assets_sold_for_repur DOUBLE COMMENT '卖出回购金融资产款', 
	frgn_currency_convert_diff DOUBLE COMMENT '外币报表折算差额', 
	general_risk_provision DOUBLE COMMENT '一般风险准备', 
	goodwill DOUBLE COMMENT '商誉', 
	held_to_maturity_invest DOUBLE COMMENT '持有至到期投资', 
	holder_equity_diff_sri DOUBLE COMMENT '股东权益差额（特殊报表科目）', 
	insurance_contract_reserve DOUBLE COMMENT '保险合同准备金', 
	intangible_assets DOUBLE COMMENT '无形资产', 
	interest_payable DOUBLE COMMENT '应付利息', 
	interest_receivable DOUBLE COMMENT '应收利息', 
	inventory DOUBLE COMMENT '存货', 
	invest_property DOUBLE COMMENT '投资性房地产', 
	lease_libilities DOUBLE COMMENT '租赁负债', 
	lending_fund DOUBLE COMMENT '拆出资金', 
	liab_and_equity_diff_sri DOUBLE COMMENT '负债及股东权益差额（特殊报表科目）', 
	liab_and_equity_diff_tbi DOUBLE COMMENT '负债及股东权益差额（合计平衡科目）', 
	liab_diff_sri DOUBLE COMMENT '负债差额（特殊报表科目）', 
	liab_diff_tbi DOUBLE COMMENT '负债差额（合计平衡科目）', 
	loan_from_central_bank DOUBLE COMMENT '向中央银行借款', 
	loans_and_payments DOUBLE COMMENT '发放贷款及垫款', 
	`It_deferred_expense` DOUBLE COMMENT '长期待摊费用', 
	`It_equity_invest` DOUBLE COMMENT '长期股权投资', 
	`It_loan` DOUBLE COMMENT '长期借款', 
	`It_payable` DOUBLE COMMENT '长期应付款', 
	`It_payable_sum` DOUBLE COMMENT '长期应付款合计', 
	`It_receivable` DOUBLE COMMENT '长期应收款', 
	`It_staff_salary_payable` DOUBLE COMMENT '长期应付职工薪酬', 
	minority_equity DOUBLE COMMENT '少数股东权益', 
	noncurrent_asset_due_within1y DOUBLE COMMENT '一年内到期的非流动资产', 
	noncurrent_assets_diff_sri DOUBLE COMMENT '非流动资产差额（特殊报表科目）', 
	noncurrent_assets_diff_tbi DOUBLE COMMENT '非流动资产差额（合计平衡科目）', 
	noncurrent_liab_diff_sbi DOUBLE COMMENT '非流动负债差额（合计平衡科目）', 
	noncurrent_liab_diff_sri DOUBLE COMMENT '非流动负债差额（特殊报表科目）', 
	noncurrent_liab_due_in1y DOUBLE COMMENT '一年内到期的非流动负债', 
	oil_and_gas_asset DOUBLE COMMENT '油气资产', 
	other_compre_fa_by_fv DOUBLE COMMENT '以公允价值计量且其变动计入其他综合收益的金融资产', 
	other_cunrren_assets DOUBLE COMMENT '其他流动资产', 
	other_current_liab DOUBLE COMMENT '其他流动负债', 
	other_debt_right_invest DOUBLE COMMENT '其他债权投资', 
	other_ei_invest DOUBLE COMMENT '其他权益工具投资', 
	other_equity_instruments DOUBLE COMMENT '其他权益工具', 
	other_payables DOUBLE COMMENT '其他应付款', 
	other_payables_sum DOUBLE COMMENT '其他应付款合计', 
	other_receivables DOUBLE COMMENT '其他应收款', 
	other_receivables_sum DOUBLE COMMENT '其他应收款合计', 
	other_uncurrent_fa DOUBLE COMMENT '其他非流动金融资产', 
	othr_noncurrent_assets DOUBLE COMMENT '其他非流动资产', 
	othr_noncurrent_liab DOUBLE COMMENT '其他非流动负债', 
	payroll_payable DOUBLE COMMENT '应付职工薪酬', 
	perpetual_capital_sec DOUBLE COMMENT '永续债', 
	preferred_shares DOUBLE COMMENT '其中优先股', 
	preferred DOUBLE COMMENT '优先股', 
	premium_receivable DOUBLE COMMENT '应收保费', 
	prepays DOUBLE COMMENT '预付款项', 
	productive_biological_assets DOUBLE COMMENT '生产性生物资产', 
	project_goods_and_material DOUBLE COMMENT '工程物资', 
	receivable_financing DOUBLE COMMENT '应收款项融资', 
	rein_account_receivable DOUBLE COMMENT '应收分保账款', 
	rein_contract_reserve DOUBLE COMMENT '应收分保合同准备金', 
	rein_payable DOUBLE COMMENT '应付分保账款', 
	right_of_use_assets DOUBLE COMMENT '使用权资产', 
	saleable_finacial_assets DOUBLE COMMENT '可供出售金融资产', 
	saving_and_interbank_deposit DOUBLE COMMENT '吸收存款及同业存放', 
	settle_reserves DOUBLE COMMENT '结算备付金', 
	special_payable DOUBLE COMMENT '专项应付款', 
	st_bond_payable DOUBLE COMMENT '应付短期债券', 
	st_borrow DOUBLE COMMENT '短期借款', 
	tax_payable DOUBLE COMMENT '应交税费', 
	total_assets DOUBLE COMMENT '资产总计', 
	total_current_assets DOUBLE COMMENT '流动资产合计', 
	total_current_liab DOUBLE COMMENT '流动负债合计', 
	total_equity_atoopc DOUBLE COMMENT '归属于母公司所有者权益合计', 
	total_liab_and_owner_equity DOUBLE COMMENT '负债和所有者权益总计', 
	total_liab DOUBLE COMMENT '负债合计', 
	total_noncurrent_assets DOUBLE COMMENT '非流动资产合计', 
	total_noncurrent_liab DOUBLE COMMENT '非流动负债合计', 
	total_owner_equity DOUBLE COMMENT '所有者权益合计', 
	tradable_fnncl_assets DOUBLE COMMENT '交易性金融资产', 
	tradable_fnncl_liab DOUBLE COMMENT '交易性金融负债', 
	treasury_stock DOUBLE COMMENT '库存股', 
	undstrbtd_profit DOUBLE COMMENT '未分配利润', 
	PRIMARY KEY (date, instrument, report_date)
)ENGINE=InnoDB COMMENT='资产负债表' DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci

/*
1 rows from balance_sheet_CN_STOCK_A table:
date	instrument	report_date	change_type	fs_quarter_index	account_receivable	accounts_payable	act_underwriting_sec	acting_td_sec	actual_received_capital	advance_payment	appropriative_reserve	asset_diff_sri	asset_diff_tbi	bill_and_account_payable	bill_and_account_receivable	bill_payable	bill_receivable	bond_payable	borrowing_funds	bs_other_compre_income	buy_resale_fnncl_assets	capital_reserve	charge_and_commi_payable	construction_in_process	construction_in_process_sum	contract_asset	contract_liab	currency_fund	debt_right_invest	derivative_fnncl_assets	derivative_fnncl_liab	dev_expenditure	differed_income_current_liab	differed_incomencl	divided_into_asset_for_sale	divided_into_liab_for_sale	dividend_payable	dividend_receivable	dt_assets	dt_liab	earned_surplus	equity_right_diff_tbi	estimated_liab	fa_calc_by_amortized_cost	fixed_asset	fixed_asset_sum	fixed_assets_disposal	flow_assets_diff_sri	flow_assets_diff_tbi	flow_debt_diff_sri	flow_debt_diff_tbi	fnncl_assets_sold_for_repur	frgn_currency_convert_diff	general_risk_provision	goodwill	held_to_maturity_invest	holder_equity_diff_sri	insurance_contract_reserve	intangible_assets	interest_payable	interest_receivable	inventory	invest_property	lease_libilities	lending_fund	liab_and_equity_diff_sri	liab_and_equity_diff_tbi	liab_diff_sri	liab_diff_tbi	loan_from_central_bank	loans_and_payments	It_deferred_expense	It_equity_invest	It_loan	It_payable	It_payable_sum	It_receivable	It_staff_salary_payable	minority_equity	noncurrent_asset_due_within1y	noncurrent_assets_diff_sri	noncurrent_assets_diff_tbi	noncurrent_liab_diff_sbi	noncurrent_liab_diff_sri	noncurrent_liab_due_in1y	oil_and_gas_asset	other_compre_fa_by_fv	other_cunrren_assets	other_current_liab	other_debt_right_invest	other_ei_invest	other_equity_instruments	other_payables	other_payables_sum	other_receivables	other_receivables_sum	other_uncurrent_fa	othr_noncurrent_assets	othr_noncurrent_liab	payroll_payable	perpetual_capital_sec	preferred_shares	preferred	premium_receivable	prepays	productive_biological_assets	project_goods_and_material	receivable_financing	rein_account_receivable	rein_contract_reserve	rein_payable	right_of_use_assets	saleable_finacial_assets	saving_and_interbank_deposit	settle_reserves	special_payable	st_bond_payable	st_borrow	tax_payable	total_assets	total_current_assets	total_current_liab	total_equity_atoopc	total_liab_and_owner_equity	total_liab	total_noncurrent_assets	total_noncurrent_liab	total_owner_equity	tradable_fnncl_assets	tradable_fnncl_liab	treasury_stock	undstrbtd_profit
2020-06-01	002986.SZA	2020-03-31	0	1	38751820.1599999964	40192764.2599999979	None	None	85000000.0000000000	55602054.5000000000	41008.8600000000	None	None	40192764.2599999979	38849820.1599999964	None	98000.0000000000	None	None	None	None	131622833.8799999952	None	None	199051890.4799999893	None	None	336463857.4200000167	None	None	None	None	None	14641535.4399999995	None	None	None	None	238529.6200000000	None	46700094.4600000009	None	None	None	None	321768063.3600000143	None	None	None	None	None	None	None	None	None	None	None	None	75680020.9699999988	None	None	82906936.5300000012	None	None	None	0E-10	0E-10	None	None	None	None	None	None	None	None	None	None	None	82500000.0000000000	None	None	None	None	None	None	None	None	None	None	None	None	None	None	6373260.2599999998	None	1198155.7000000000	None	None	None	12962158.5299999993	None	None	None	None	284380461.5099999905	None	None	None	None	None	None	None	None	None	None	None	None	None	-8359396.1699999999	1345800666.7899000645	746799231.3200000525	106770841.3799999952	1012298131.1900000572	1345800666.7899999619	251002535.5999999940	599001435.4700000286	144231694.2199999988	1094798131.1900000572	3000000.0000000000	None	None	748934193.9900000095
*/


CREATE TABLE `basic_info_CN_STOCK_A` (
	instrument VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '证券代码', 
	delist_date DATE COMMENT '退市日期，如果未退市，则为pandas.NaT', 
	company_type VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '公司类型', 
	company_name VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '公司名称', 
	company_province VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '公司省份', 
	list_board VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '上市板', 
	company_found_date DATETIME COMMENT '公司成立日期', 
	name VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '证券名称', 
	list_date DATE COMMENT '上市日期', 
	PRIMARY KEY (instrument)
)ENGINE=InnoDB COMMENT='A股股票基本信息' DEFAULT CHARSET=utf8mb3

/*
1 rows from basic_info_CN_STOCK_A table:
instrument	delist_date	company_type	company_name	company_province	list_board	company_found_date	name	list_date
000001.SZA	None	公众企业	平安银行股份有限公司	广东省	主板	1987-12-22 00:00:00	平安银行	1991-04-03
*/


CREATE TABLE `cash_flow_CN_STOCK_A` (
	date DATE COMMENT '公告日', 
	instrument VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '股票代码', 
	report_date DATE COMMENT '报告期', 
	change_type INTEGER COMMENT '调整类型 0：未调整，1：调整过', 
	fs_quarter_index INTEGER COMMENT '对应季度', 
	asset_impairment_reserve DOUBLE COMMENT '资产减值准备', 
	borrowing_net_add_central_bank DOUBLE COMMENT '向中央银行借款净增加额', 
	borrowing_net_increase_amt DOUBLE COMMENT '拆入资金净增加额', 
	cash_of_orig_ic_indemnity DOUBLE COMMENT '支付原保险合同赔付款项的现金', 
	cash_paid_for_assets DOUBLE COMMENT '购建固定资产、无形资产和其他长期资产支付的现金', 
	cash_paid_for_interests_etc DOUBLE COMMENT '支付利息、手续费及佣金的现金', 
	cash_paid_for_pd DOUBLE COMMENT '支付保单红利的现金', 
	cash_paid_of_distribution DOUBLE COMMENT '分配股利、利润或偿付利息支付的现金', 
	cash_paid_to_staff_etc DOUBLE COMMENT '支付给职工以及为职工支付的现金', 
	cash_pay_for_debt DOUBLE COMMENT '偿还债务支付的现金', 
	cash_received_from_bond_issue DOUBLE COMMENT '发行债券收到的现金', 
	cash_received_from_orig_ic DOUBLE COMMENT '收到原保险合同保费取得的现金', 
	cash_received_of_absorb_invest DOUBLE COMMENT '吸收投资收到的现金', 
	cash_received_of_borrowing DOUBLE COMMENT '取得借款收到的现金', 
	cash_received_of_dspsl_invest DOUBLE COMMENT '收回投资收到的现金', 
	cash_received_of_interest_etc DOUBLE COMMENT '收取利息、手续费及佣金的现金', 
	cash_received_of_other_fa DOUBLE COMMENT '收到其他与投资活动有关的现金', 
	cash_received_of_other_oa DOUBLE COMMENT '收到其他与经营活动有关的现金', 
	cash_received_of_othr_fa DOUBLE COMMENT '收到其他与筹资活动有关的现金', 
	cash_received_of_sales_service DOUBLE COMMENT '销售商品、提供劳务收到的现金', 
	cb_due_within1y DOUBLE COMMENT '一年内到期的可转换公司债券', 
	cce_net_add_amt_diff_sri_dm DOUBLE COMMENT '直接法—现金及现金等价物净增加额差额（特殊报表科目）', 
	cce_net_add_amt_diff_tbi_dm DOUBLE COMMENT '直接法—现金及现金等价物净增加额差额（合计平衡科目）', 
	cce_net_add_diff_im_sri DOUBLE COMMENT '间接法—现金及现金等价物净增加额差额（特殊报表科目）', 
	cce_net_add_diff_im_tbi DOUBLE COMMENT '间接法—现金及现金等价物净增加额差额（合计平衡科目）', 
	cr_from_minority_holders DOUBLE COMMENT '子公司吸收少数股东投资收到的现金', 
	credit_impairment_loss DOUBLE COMMENT '信用减值损失', 
	dap_paid_to_minority_holder DOUBLE COMMENT '子公司支付给少数股东的股利、利润', 
	debt_tranfer_to_capital DOUBLE COMMENT '债务转为资本', 
	deposit_and_interbank_net_add DOUBLE COMMENT '客户存款和同业存放款项净增加额', 
	depreciation_etc DOUBLE COMMENT '固定资产折旧、油气资产折耗、生产性生物资产折旧', 
	dt_assets_decrease DOUBLE COMMENT '递延所得税资产减少', 
	dt_liab_increase DOUBLE COMMENT '递延所得税负债增加', 
	effect_of_exchange_chg_on_cce DOUBLE COMMENT '汇率变动对现金及现金等价物的影响', 
	ending_balance_of_cash DOUBLE COMMENT '现金的期末余额', 
	fa_cash_in_flow_diff_sri DOUBLE COMMENT '筹资活动现金流入差额（特殊报表科目）', 
	fa_cash_in_flow_diff_tbi DOUBLE COMMENT '筹资活动现金流入差额（合计平衡科目）', 
	fa_cash_out_flow_diff_sri DOUBLE COMMENT '筹资活动现金流出差额（特殊报表科目）', 
	fa_cash_out_flow_diff_tbi DOUBLE COMMENT '筹资活动现金流出差额（合计平衡科目）', 
	final_balance_of_cce DOUBLE COMMENT '期末现金及现金等价物余额', 
	finance_cost_cfs DOUBLE COMMENT '现金流量表—财务费用', 
	finance_lease_fixed_assets DOUBLE COMMENT '融资租入固定资产', 
	fixed_assets_scrap_loss DOUBLE COMMENT '固定资产报废损失', 
	goods_buy_and_service_cash_pay DOUBLE COMMENT '购买商品、接受劳务支付的现金', 
	ia_cash_inflow_diff_sri DOUBLE COMMENT '投资活动现金流入差额（特殊报表科目）', 
	ia_cash_inflow_diff_tbi DOUBLE COMMENT '投资活动现金流入差额（合计平衡科目）', 
	ia_cash_outflow_diff_sri DOUBLE COMMENT '投资活动现金流出差额（特殊报表科目）', 
	ia_cash_outflow_diff_tbi DOUBLE COMMENT '投资活动现金流出差额（合计平衡科目）', 
	increase_of_operating_item DOUBLE COMMENT '经营性应付项目的增加', 
	initial_balance_of_cash DOUBLE COMMENT '现金的期初余额', 
	initial_balance_of_cce DOUBLE COMMENT '现金等价物的期初余额', 
	initial_cce_balance DOUBLE COMMENT '期初现金及现金等价物余额', 
	intangible_assets_amortized DOUBLE COMMENT '无形资产摊销', 
	inventory_decrease DOUBLE COMMENT '存货的减少', 
	invest_income_cash_received DOUBLE COMMENT '取得投资收益收到的现金', 
	invest_loss DOUBLE COMMENT '投资损失', 
	invest_paid_cash DOUBLE COMMENT '投资支付的现金', 
	lending_net_add_other_org DOUBLE COMMENT '向其他金融机构拆入资金净增加额', 
	loan_and_advancenet_add DOUBLE COMMENT '客户贷款及垫款净增加额', 
	loss_from_fv_chg DOUBLE COMMENT '公允价值变动损失', 
	loss_of_disposal_assets DOUBLE COMMENT '处置固定资产、无形资产和其他长期资产的损失', 
	`It_deferred_expenses_amrtzt` DOUBLE COMMENT '长期待摊费用摊销', 
	naa_of_cb_and_interbank DOUBLE COMMENT '存放中央银行和同业款项净增加额', 
	naa_of_disposal_fnncl_assets DOUBLE COMMENT '处置以公允价值计量且其变动计入当期损益的金融资产净增加额', 
	naaassured_saving_and_invest DOUBLE COMMENT '保户储金及投资款净增加额', 
	ncf_diff_from_fa_sri DOUBLE COMMENT '筹资活动产生的现金流量净额差额（特殊报表科目）', 
	ncf_diff_from_fa_tbi DOUBLE COMMENT '筹资活动产生的现金流量净额差额（合计平衡科目）', 
	ncf_diff_from_ia_sri DOUBLE COMMENT '投资活动产生的现金流量净额差额（特殊报表科目）', 
	ncf_diff_from_ia_tbi DOUBLE COMMENT '投资活动产生的现金流量净额差额（合计平衡科目）', 
	ncf_diff_from_oa_im_sri DOUBLE COMMENT '间接法—经营活动现金流量净额差额（特殊报表科目）', 
	ncf_diff_from_oa_im_tbi DOUBLE COMMENT '间接法—经营活动现金流量净额差额（合计平衡科目）', 
	ncf_diff_of_oa_sri DOUBLE COMMENT '经营活动产生的现金流量净额差额（特殊报表科目）', 
	ncf_diff_of_oa_tbi DOUBLE COMMENT '经营活动产生的现金流量净额差额（合计平衡科目）', 
	ncf_from_fa DOUBLE COMMENT '筹资活动产生的现金流量净额', 
	ncf_from_ia DOUBLE COMMENT '投资活动产生的现金流量净额', 
	ncf_from_oa_im DOUBLE COMMENT '间接法—经营活动产生的现金流量净额', 
	ncf_from_oa DOUBLE COMMENT '经营活动产生的现金流量净额', 
	net_add_in_pledge_loans DOUBLE COMMENT '质押贷款净增加额', 
	net_add_in_repur_capital DOUBLE COMMENT '回购业务资金净增加额', 
	net_cash_amt_from_branch DOUBLE COMMENT '取得子公司及其他营业单位支付的现金净额', 
	net_cash_of_disposal_assets DOUBLE COMMENT '处置固定资产、无形资产和其他长期资产收回的现金净额', 
	net_cash_of_disposal_branch DOUBLE COMMENT '处置子公司及其他营业单位收到的现金净额', 
	net_cash_received_from_rein DOUBLE COMMENT '收到再保业务现金净额', 
	net_increase_in_cce_im DOUBLE COMMENT '间接法—现金及现金等价物净增加额', 
	net_increase_in_cce DOUBLE COMMENT '现金及现金等价物净增加额', 
	np_cfs DOUBLE COMMENT '现金流量表-净利润', 
	oa_cash_inflow_diff_sri DOUBLE COMMENT '经营活动现金流入差额（特殊报表科目）', 
	oa_cash_inflow_diff_tbi DOUBLE COMMENT '经营活动现金流入差额（合计平衡科目）', 
	oa_cash_outflow_diff_sri DOUBLE COMMENT '经营活动现金流出差额（特殊报表科目）', 
	oa_cash_outflow_diff_tbi DOUBLE COMMENT '经营活动现金流出差额（合计平衡科目）', 
	operating_items_decrease DOUBLE COMMENT '经营性应收项目的减少', 
	other_cash_paid_related_to_ia DOUBLE COMMENT '支付其他与投资活动有关的现金', 
	other_cash_paid_related_to_oa DOUBLE COMMENT '支付其他与经营活动有关的现金', 
	othrcash_paid_relating_to_fa DOUBLE COMMENT '支付其他与筹资活动有关的现金', 
	payments_of_all_taxes DOUBLE COMMENT '支付的各项税费', 
	refund_of_tax_and_levies DOUBLE COMMENT '收到的税费返还', 
	si_final_balance_of_cce DOUBLE COMMENT '现金等价物的期末余额', 
	si_other DOUBLE COMMENT '其他', 
	sub_total_of_ci_from_fa DOUBLE COMMENT '筹资活动现金流入小计', 
	sub_total_of_ci_from_ia DOUBLE COMMENT '投资活动现金流入小计', 
	sub_total_of_ci_from_oa DOUBLE COMMENT '经营活动现金流入小计', 
	sub_total_of_cos_from_fa DOUBLE COMMENT '筹资活动现金流出小计', 
	sub_total_of_cos_from_ia DOUBLE COMMENT '投资活动现金流出小计', 
	sub_total_of_cos_from_oa DOUBLE COMMENT '经营活动现金流出小计'
)ENGINE=InnoDB COMMENT='现金流量表' DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci

/*
1 rows from cash_flow_CN_STOCK_A table:
date	instrument	report_date	change_type	fs_quarter_index	asset_impairment_reserve	borrowing_net_add_central_bank	borrowing_net_increase_amt	cash_of_orig_ic_indemnity	cash_paid_for_assets	cash_paid_for_interests_etc	cash_paid_for_pd	cash_paid_of_distribution	cash_paid_to_staff_etc	cash_pay_for_debt	cash_received_from_bond_issue	cash_received_from_orig_ic	cash_received_of_absorb_invest	cash_received_of_borrowing	cash_received_of_dspsl_invest	cash_received_of_interest_etc	cash_received_of_other_fa	cash_received_of_other_oa	cash_received_of_othr_fa	cash_received_of_sales_service	cb_due_within1y	cce_net_add_amt_diff_sri_dm	cce_net_add_amt_diff_tbi_dm	cce_net_add_diff_im_sri	cce_net_add_diff_im_tbi	cr_from_minority_holders	credit_impairment_loss	dap_paid_to_minority_holder	debt_tranfer_to_capital	deposit_and_interbank_net_add	depreciation_etc	dt_assets_decrease	dt_liab_increase	effect_of_exchange_chg_on_cce	ending_balance_of_cash	fa_cash_in_flow_diff_sri	fa_cash_in_flow_diff_tbi	fa_cash_out_flow_diff_sri	fa_cash_out_flow_diff_tbi	final_balance_of_cce	finance_cost_cfs	finance_lease_fixed_assets	fixed_assets_scrap_loss	goods_buy_and_service_cash_pay	ia_cash_inflow_diff_sri	ia_cash_inflow_diff_tbi	ia_cash_outflow_diff_sri	ia_cash_outflow_diff_tbi	increase_of_operating_item	initial_balance_of_cash	initial_balance_of_cce	initial_cce_balance	intangible_assets_amortized	inventory_decrease	invest_income_cash_received	invest_loss	invest_paid_cash	lending_net_add_other_org	loan_and_advancenet_add	loss_from_fv_chg	loss_of_disposal_assets	It_deferred_expenses_amrtzt	naa_of_cb_and_interbank	naa_of_disposal_fnncl_assets	naaassured_saving_and_invest	ncf_diff_from_fa_sri	ncf_diff_from_fa_tbi	ncf_diff_from_ia_sri	ncf_diff_from_ia_tbi	ncf_diff_from_oa_im_sri	ncf_diff_from_oa_im_tbi	ncf_diff_of_oa_sri	ncf_diff_of_oa_tbi	ncf_from_fa	ncf_from_ia	ncf_from_oa_im	ncf_from_oa	net_add_in_pledge_loans	net_add_in_repur_capital	net_cash_amt_from_branch	net_cash_of_disposal_assets	net_cash_of_disposal_branch	net_cash_received_from_rein	net_increase_in_cce_im	net_increase_in_cce	np_cfs	oa_cash_inflow_diff_sri	oa_cash_inflow_diff_tbi	oa_cash_outflow_diff_sri	oa_cash_outflow_diff_tbi	operating_items_decrease	other_cash_paid_related_to_ia	other_cash_paid_related_to_oa	othrcash_paid_relating_to_fa	payments_of_all_taxes	refund_of_tax_and_levies	si_final_balance_of_cce	si_other	sub_total_of_ci_from_fa	sub_total_of_ci_from_ia	sub_total_of_ci_from_oa	sub_total_of_cos_from_fa	sub_total_of_cos_from_ia	sub_total_of_cos_from_oa
2021-06-01	001207.SZA	2021-03-31	0	4	None	None	None	None	10181123.6300000008	None	None	1459820.4099999999	19302293.2899999991	None	None	None	None	None	275038853.4599999785	None	None	5664507.9299999997	None	190139593.4499999881	None	None	None	None	None	None	4222312.5499999998	None	None	None	None	None	None	41163.6600000000	None	None	None	None	None	29451747.8599999994	None	None	None	174371121.3100000024	None	None	None	None	None	None	None	71074349.3100000024	None	None	176566.3500000000	None	287048297.0000000000	None	None	None	None	None	None	None	None	None	0E-10	None	0E-10	None	None	None	0E-10	-1459820.4099999999	-22014000.8200000003	None	-18189943.8799999990	None	None	None	None	None	None	None	-41622601.4500000030	None	None	None	None	None	None	None	11533272.3900000006	None	13205598.1600000001	4418239.8899999997	None	None	None	275215419.8100000024	200222341.2700000107	1459820.4099999999	297229420.6299999952	218412285.1500000060
*/


CREATE TABLE `income_CN_STOCK_A` (
	date DATE COMMENT '日期', 
	instrument VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '股票代码', 
	report_date DATE COMMENT '报告期', 
	change_type INTEGER COMMENT '调整类型 (0: 未调整, 1: 调整过)', 
	fs_quarter_index INTEGER COMMENT '对应季度', 
	amortized_cost_fnncl_ass_cfrm DOUBLE COMMENT '以摊余成本计量的金融资产终止确认收益', 
	asset_change_due_to_remeasure DOUBLE COMMENT '重新计量设定受益计划净负债或净资产的变动', 
	asset_disposal_gain DOUBLE COMMENT '资产处置收益', 
	asset_impairment_loss DOUBLE COMMENT '资产减值损失', 
	basic_eps DOUBLE COMMENT '基本每股收益', 
	cannt_reclass_gal_equity_law DOUBLE COMMENT '权益法下在被投资单位不能重分类进损益的其他综合收益中享有的份额', 
	cannt_reclass_to_gal DOUBLE COMMENT '以后不能重分类进损益的其他综合收益', 
	cash_flow_hedge_reserve DOUBLE COMMENT '现金流量套期储备', 
	cf_hedging_gal_valid_part DOUBLE COMMENT '现金流量套期损益的有效部分', 
	charge_and_commi_expenses DOUBLE COMMENT '手续费及佣金支出', 
	commi_on_insurance_policy DOUBLE COMMENT '保单红利支出', 
	compensate_net_pay DOUBLE COMMENT '赔付支出净额', 
	continued_operating_np DOUBLE COMMENT '（一）持续经营净利润', 
	corp_credit_risk_fvc DOUBLE COMMENT '企业自身信用风险公允价值变动', 
	credit_impairment_loss DOUBLE COMMENT '信用减值损失', 
	dlt_earnings_per_share DOUBLE COMMENT '稀释每股收益', 
	earned_premium DOUBLE COMMENT '已赚保费', 
	exchange_gain DOUBLE COMMENT '汇兑收益', 
	extract_ic_reserve_net_amt DOUBLE COMMENT '提取保险合同准备金净额', 
	fa_reclassi_amt DOUBLE COMMENT '金融资产重分类计入其他综合收益的金额', 
	fc_convert_diff DOUBLE COMMENT '外币财务报表折算差额', 
	fc_interest_income DOUBLE COMMENT '财务费用：利息收入', 
	fee_and_commi_income DOUBLE COMMENT '手续费及佣金收入', 
	financing_expenses DOUBLE COMMENT '财务费用', 
	fv_chg_income DOUBLE COMMENT '公允价值变动收益', 
	ii_from_jc_etc DOUBLE COMMENT '对联营企业和合营企业的投资收益', 
	income_tax_cost DOUBLE COMMENT '所得税费用', 
	interest_fee DOUBLE COMMENT '财务费用：利息费用', 
	interest_income DOUBLE COMMENT '利息收入', 
	interest_payout DOUBLE COMMENT '利息支出', 
	invest_income DOUBLE COMMENT '投资收益', 
	manage_fee DOUBLE COMMENT '管理费用', 
	minority_gal DOUBLE COMMENT '少数股东损益', 
	net_open_hedge_income DOUBLE COMMENT '净敞口套期收益', 
	non_operating_income DOUBLE COMMENT '营业外收入', 
	noncurrent_asset_dispose_gain DOUBLE COMMENT '非流动资产处置利得', 
	noncurrent_asset_dispose_loss DOUBLE COMMENT '非流动资产处置损失', 
	nonoperating_cost DOUBLE COMMENT '营业外支出', 
	np_atoopc DOUBLE COMMENT '归属于母公司所有者的净利润', 
	np_diff_sri DOUBLE COMMENT '净利润差额（特殊报表科目）', 
	np_diff_tbi DOUBLE COMMENT '净利润差额（合计平衡科目）', 
	op_diff_sri DOUBLE COMMENT '营业利润差额（特殊报表科目）', 
	op_diff_tbi DOUBLE COMMENT '营业利润差额（合计平衡科目）', 
	operating_cost_diff_sri DOUBLE COMMENT '营业支出（特殊报表科目）', 
	operating_cost_diff_tbi DOUBLE COMMENT '营业支出（合计平衡项目）', 
	operating_cost DOUBLE COMMENT '营业成本', 
	operating_revenue_diff_sri DOUBLE COMMENT '营业收入（特殊报表科目）', 
	operating_revenue_diff_tbi DOUBLE COMMENT '营业收入（合计平衡项目）', 
	operating_taxes_and_surcharge DOUBLE COMMENT '税金及附加', 
	operating_total_cost DOUBLE COMMENT '营业总成本', 
	operating_total_revenue DOUBLE COMMENT '营业总收入', 
	other_compre_income DOUBLE COMMENT '其他综合收益', 
	other_debt_right_invest_fvc DOUBLE COMMENT '其他债权投资公允价值变动', 
	other_debt_right_invest_ir DOUBLE COMMENT '其他债权投资信用减值准备', 
	other_equity_invest_fvc DOUBLE COMMENT '其他权益工具投资公允价值变动', 
	other_income DOUBLE COMMENT '其他收益', 
	other_not_reclass_to_gal DOUBLE COMMENT '其他以后不能重分类进损益', 
	other_reclass_to_gal DOUBLE COMMENT '其他以后将重分类进损益', 
	othrcompre_income_atms DOUBLE COMMENT '归属于少数股东的其他综合收益', 
	othrcompre_income_atoopc DOUBLE COMMENT '归属母公司所有者的其他综合收益', 
	rad_cost_sum DOUBLE COMMENT '研发费用', 
	reclass_and_salable_gal DOUBLE COMMENT '持有至到期投资重分类为可供出售金融资产损益', 
	reclass_to_gal DOUBLE COMMENT '以后将重分类进损益的其他综合收益', 
	reclass_togal_in_equity_law DOUBLE COMMENT '权益法下在被投资单位以后将重分类进损益的其他综合收益中享有的份额', 
	refunded_premium DOUBLE COMMENT '退保金', 
	rein_expenditure DOUBLE COMMENT '分保费用', 
	revenue DOUBLE COMMENT '营业收入', 
	saleable_fv_chg_gal DOUBLE COMMENT '可供出售金融资产公允价值变动损益', 
	sales_fee DOUBLE COMMENT '销售费用', 
	stop_operating_np DOUBLE COMMENT '（二）终止经营净利润', 
	total_compre_income_atsopc DOUBLE COMMENT '归属于母公司股东的综合收益总额', 
	total_compre_income DOUBLE COMMENT '综合收益总额', 
	total_profit_diff_sri DOUBLE COMMENT '利润总额差额（特殊报表科目）', 
	total_profit_diff_tbi DOUBLE COMMENT '利润总额差额（合计平衡科目）', 
	total_profit DOUBLE COMMENT '利润总额'
)ENGINE=InnoDB COMMENT='利润表' DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci

/*
1 rows from income_CN_STOCK_A table:
date	instrument	report_date	change_type	fs_quarter_index	amortized_cost_fnncl_ass_cfrm	asset_change_due_to_remeasure	asset_disposal_gain	asset_impairment_loss	basic_eps	cannt_reclass_gal_equity_law	cannt_reclass_to_gal	cash_flow_hedge_reserve	cf_hedging_gal_valid_part	charge_and_commi_expenses	commi_on_insurance_policy	compensate_net_pay	continued_operating_np	corp_credit_risk_fvc	credit_impairment_loss	dlt_earnings_per_share	earned_premium	exchange_gain	extract_ic_reserve_net_amt	fa_reclassi_amt	fc_convert_diff	fc_interest_income	fee_and_commi_income	financing_expenses	fv_chg_income	ii_from_jc_etc	income_tax_cost	interest_fee	interest_income	interest_payout	invest_income	manage_fee	minority_gal	net_open_hedge_income	non_operating_income	noncurrent_asset_dispose_gain	noncurrent_asset_dispose_loss	nonoperating_cost	np_atoopc	np_diff_sri	np_diff_tbi	op_diff_sri	op_diff_tbi	operating_cost_diff_sri	operating_cost_diff_tbi	operating_cost	operating_revenue_diff_sri	operating_revenue_diff_tbi	operating_taxes_and_surcharge	operating_total_cost	operating_total_revenue	other_compre_income	other_debt_right_invest_fvc	other_debt_right_invest_ir	other_equity_invest_fvc	other_income	other_not_reclass_to_gal	other_reclass_to_gal	othrcompre_income_atms	othrcompre_income_atoopc	rad_cost_sum	reclass_and_salable_gal	reclass_to_gal	reclass_togal_in_equity_law	refunded_premium	rein_expenditure	revenue	saleable_fv_chg_gal	sales_fee	stop_operating_np	total_compre_income_atsopc	total_compre_income	total_profit_diff_sri	total_profit_diff_tbi	total_profit
2020-06-01	002986.SZA	2020-03-31	0	1	None	None	None	None	0.3200000000	None	None	None	None	None	None	None	27147565.3399999999	None	None	0.3200000000	None	None	None	None	None	-208159.5400000000	None	-616915.6300000000	None	None	953703.1400000000	None	None	None	244535.1100000000	4581845.3799999999	None	None	481074.1000000000	None	None	298543.0200000000	27147565.3399999999	None	None	None	None	None	None	547983896.0800000429	None	None	404801.2800000000	575306136.9500000477	598151678.9199999571	None	None	None	None	4828660.3200000003	None	None	None	None	18352213.1900000013	None	None	None	None	None	598151678.9199999571	None	4600296.6500000004	None	27147565.3399999999	27147565.3399999999	None	None	28101268.4800000004'''