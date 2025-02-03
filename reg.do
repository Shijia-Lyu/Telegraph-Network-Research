import "/Users/lvshijia/Downloads/provincial_base.dta"
gen running_variable = year - 1900
gen treatment = running_variable >= 0
rdrobust revo_count running_variable, c(0) covs(tele_count) p(1)
rdrobust revo_count year, c(1900)
twoway (scatter revo_count year) (lfit revo_count year if year < 1900) (lfit revo_count year if year >= 1900)
rdrobust tele_count year, c(1900)
twoway (scatter tele_count year) (lfit tele_count year if year < 1900) (lfit tele_count year if year >= 1900)
rdplot tele year, c(1900)
graph save graph1.gph, replace
rdplot revo_group year, c(1900)
graph save graph2.gph, replace
graph combine graph1.gph graph2.gph, col(1)
graph combine graph1.gph graph2.gph, col(1) title("Telegram and Revolution Group")
reg rice_price tele
reg revo_group rice_price
reg revo_group rice_price price_level
reg revo_group tele revo_2 rice_price price_level


