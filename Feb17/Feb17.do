reg revo_group tele
est store revo1
reg revo_group tele ln_pop ln_size south price_level rice_price
est store revo2
reg revo_group tele ln_pop ln_size south treaty rice_price price_level
est store revo3
reg revo_group tele ln_quota ln_pop ln_size south treaty price_level rice_price
est store revo4
esttab revo1 revo2 revo3 revo4 using estReg1.tex, booktabs b(%8.4f) se(%8.4f) star(* 0.1 ** 0.05 *** 0.001) stats(aic bic N r2 r2_a F ll) nogap replace mtitle("Model1" "Model2" "Model3" "Model4" "FE") order(revo_group tele treaty ln_pop ln_size ln_quota south price_level rice_price )

gen running_variable = year - 1900
gen treatment = running_variable >= 0
rdrobust revo_group year, c(1900) p(1) kernel(tri)
rdplot tele year, c(1900)
graph save graph1.gph, replace
rdplot revo_group year, c(1900)
graph save graph2.gph, replace
graph combine graph1.gph graph2.gph, col(1)
graph combine graph1.gph graph2.gph, col(1) title("Telegram and Revolution Group")
graph export "C:\Users\11786\OneDrive\桌面\Graph.png", as(png) name("Graph")

#时间固定效应模型
#reg revo_group tele i.year （一种方式）
areg revo_group tele, a(year)

#时间地点固定效应模型
 areg revo_group tele i.id, a(year)
 
 #处理异方差问题
 areg revo_group tele i.id, a(year) robust
   #聚类稳健标准误、
 areg revo_group tele i.id, a(year) cluster(location2)
 
 #交叉项
  areg revo_group tele c.tele#c.ln_pop i.id, a(year) cluster(location2)

