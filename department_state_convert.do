//generate categorical variables for departments
encode department_name, gen(department_category)
gen d_category=int(department_category)

//generate categorical variables for states
encode state_name, gen(state_category)
gen s_category=int(state_category)

