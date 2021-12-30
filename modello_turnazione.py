import time
import pyomo.environ as py
import math
import sys

def checkPatternMatching(s, pattern):
    if len(pattern) == 3:
        max_matchingValue = 0
        for start in range(0, 2):
            matchingCounter = 0

            for i in range(start, 3 + start):
                if str(pattern[i - start]) == s[i]:
                    matchingCounter += 1
            matchingValue = matchingCounter / 3

            if matchingValue > max_matchingValue:
                max_matchingValue = matchingValue

    elif len(pattern) == 4:
        matchingCounter = 0

        for i in range(0, 4):
            if str(pattern[i]) == s[i]:
                matchingCounter += 1

        max_matchingValue = matchingCounter / 4

    return max_matchingValue

def searchPossibilePatterns(assignment, operators, days):
    patterns = {}
    days_array = [d for d in days]

    patterns[0] = [(1, 1, 2), 97]
    patterns[1] = [(2, 4, 4), 93]
    patterns[2] = [(1, 2, 2), 90]
    patterns[3] = [(1, 1, 1), 90]
    patterns[4] = [(4, 4, 1, 1), 87]
    patterns[5] = [(2, 2, 4, 4), 78]
    patterns[6] = [(1, 1, 4), 75]
    patterns[7] = [(2, 2, 2), 74]

    bestPattern = None
    sequence = None
    operator = None
    maxMatchingValue = 0

    for p in operators:
        for d in days_array[0:len(days_array) - 3]:
            s = ""

            for i in range(d, d + 4):
                s += str(assignment[p, i])

            for pattern in patterns.values():
                matchingValue = checkPatternMatching(s, pattern[0])

                if maxMatchingValue < matchingValue and matchingValue < 1.0:
                    sequence = (d, d + 4)
                    bestPattern = pattern
                    maxMatchingValue = matchingValue
                    operator = p
                elif maxMatchingValue == matchingValue and maxMatchingValue > 0.0:
                    if pattern[1] > bestPattern[1]:
                        sequence = (d, d + 4)
                        bestPattern = pattern
                        operator = p

    print(str(bestPattern[0]))

    for i in range(sequence[0], sequence[1]):
        print(str(assignment[operator, i]), end=" ")

    print("\n")
    print(maxMatchingValue)
    print("\n")


solver_name = 'cplex'
solver_path = 'C:\\Program Files\IBM\ILOG\CPLEX_Studio1210\cplex\\bin\\x64_win64\cplex.exe'

model = py.AbstractModel()

# parametri
model.p = py.Param(within=py.PositiveIntegers)
model.d = py.Param(within=py.PositiveIntegers)
model.f = py.Param(within=py.PositiveIntegers)
model.t = py.Param(within=py.PositiveIntegers)
model.wh = py.Param(within=py.PositiveIntegers)
# model.th = py.Param(within=py.PositiveIntegers)

model.P = py.RangeSet(1, model.p)
model.D = py.RangeSet(1, model.d)
model.F = py.RangeSet(1, model.f)
model.T = py.RangeSet(1, model.t)

model.S = py.Param(model.T, model.D, within=py.NonNegativeIntegers)
model.AV = py.Param(model.P, model.D, within=py.Boolean)
model.B = py.Param(model.P, model.D, within=py.Boolean)
model.O = py.Param(model.P, model.D, within=py.Boolean)
model.N = py.Param(model.P, model.D, within=py.Boolean)
model.V = py.Param(model.P, model.D, within=py.Boolean)
model.Z = py.Param(model.P, model.D, within=py.Boolean)
model.J = py.Param(model.P, model.D, within=py.Boolean)
model.L = py.Param(model.P, model.D, within=py.Boolean)
model.G = py.Param(model.P, model.D, within=py.Boolean)
model.E = py.Param(model.P, model.D, within=py.Boolean)
model.R = py.Param(model.P, model.D, within=py.Boolean)
model.U = py.Param(model.P, model.D, within=py.Boolean)
model.H = py.Param(model.T, within=py.NonNegativeReals)
model.W = py.Param(model.F, within=py.PositiveIntegers)
model.Q = py.Param(model.P, model.D, within=py.Boolean)
model.SO = py.Param(model.P, within=py.Boolean)
model.OH = py.Param(model.P, within=py.NonNegativeIntegers)
model.MH = py.Param(model.P, within=py.NonNegativeIntegers)
model.COEFF = py.Param(model.P, model.D, within=py.NonNegativeIntegers)

# variabili
model.x = py.Var(model.P, model.D, model.T, domain=py.Boolean, initialize=0)
model.y = py.Var(model.P, domain=py.NonNegativeReals, initialize=0)
model.b = py.Var(model.P, model.F, domain=py.NonNegativeIntegers, initialize=0)
model.psi = py.Var(model.P, model.D, domain=py.NonNegativeIntegers, initialize=0)
model.k = py.Var(model.P, model.D, domain=py.Boolean, initialize=0)
model.sigma = py.Var(model.P, model.D, domain=py.Boolean, initialize=0)
model.gamma = py.Var(model.P, model.D, domain=py.Boolean, initialize=0)
model.a = py.Var(domain=py.NonNegativeReals, initialize=0)
model.phi = py.Var(model.F, domain=py.NonNegativeIntegers, initialize=0)
model.mu = py.Var(model.P, domain=py.NonNegativeIntegers, initialize=0)
# model.phi = py.Var(domain=py.NonNegativeIntegers, initialize=0)

# funzione obiettivo
def obj_func(mod):
   v1 = 0.30
   v2 = 0.05
   v3 = 0.20
   v4 = 0.05
   v5 = 0.40
   v6 = 0.05

   l1 = 0.80
   l2 = 0.15
   l3 = 0.05

   return v1 * mod.a +\
          v2 * sum(sum(mod.b[p, f] for f in mod.F) for p in mod.P) -\
          v3 * sum((l1 * sum(mod.x[p, d, 1] for p in mod.P) + l2 * sum(mod.x[p, d, 2] for p in mod.P) + l3 * sum(mod.x[p, d, 3] for p in mod.P)) for d in mod.D)-\
          v4 * sum(sum(mod.sigma[p, d] for d in mod.D) for p in  mod.P) +\
          v5 * sum(mod.phi[f] for f in mod.F) +\
          v6 * sum(sum(mod.COEFF[p, d] * mod.x[p, d, 5] for d in mod.D) + (math.factorial(mod.d - 1) / math.factorial(mod.d - mod.OH[p] - 1) + 1) * mod.mu[p] for p in mod.P)
model.obj_func = py.Objective(rule=obj_func, sense=py.minimize)

# vincoli
def work_hours(mod, p):
   return sum(sum(mod.x[p, d, t] * mod.H[t] for t in mod.T) for d in mod.D) == mod.y[p]
model.work_hours = py.Constraint(model.P, rule=work_hours)

def minimum_morning_operators(mod, d):
   return sum(mod.x[p, d, 1] + mod.x[p, d, 9] for p in mod.P) >= mod.S[1, d]
model.minimum_morning_operators = py.Constraint(model.D, rule=minimum_morning_operators)

def minimum_afternoon_operators(mod, d):
   return sum(mod.x[p, d, 2] + mod.x[p, d, 10] for p in mod.P) >= mod.S[2, d]
model.minimum_afternoon_operators = py.Constraint(model.D, rule=minimum_afternoon_operators)

def minimum_night_operators(mod, d):
   return sum(mod.x[p, d, 3] for p in mod.P) >= mod.S[3, d]
model.minimum_night_operators = py.Constraint(model.D, rule=minimum_night_operators)

def night_availabilty(mod, p, d):
    if mod.SO[p] == 1:
        return mod.x[p, d, 3] <= mod.AV[p, d]
    else:
        return py.Constraint.Skip
model.night_availabilty = py.Constraint(model.P, model.D, rule=night_availabilty)

def morning_preassignment(mod, p, d):
    if mod.SO[p] == 1:
        return mod.x[p, d, 1] >= mod.B[p, d]
    else:
        return py.Constraint.Skip
model.morning_preassignment = py.Constraint(model.P, model.D, rule=morning_preassignment)

def afternoon_preassignment(mod, p, d):
    if mod.SO[p] == 1:
        return mod.x[p, d, 2] >= mod.O[p, d]
    else:
        return py.Constraint.Skip
model.afternoon_preassignment = py.Constraint(model.P, model.D, rule=afternoon_preassignment)

def night_preassignment(mod, p, d):
    if mod.SO[p] == 0:
        return mod.x[p, d, 3] >= mod.N[p, d]
    else:
        return py.Constraint.Skip
model.night_preassignment = py.Constraint(model.P, model.D, rule=night_preassignment)

def rest_preassignment(mod, p, d):
    return mod.x[p, d, 4] >= mod.V[p, d]
model.rest_preassignment = py.Constraint(model.P, model.D, rule=rest_preassignment)

def mandatory_holidays_preassignment(mod, p, d):
    return mod.x[p, d, 5] >= mod.Q[p, d]
model.mandatory_holidays_preassignment = py.Constraint(model.P, model.D, rule=mandatory_holidays_preassignment)

def study_permit(mod, p, d):
    return mod.x[p, d, 6] == mod.Z[p, d]
model.study_permit = py.Constraint(model.P, model.D, rule=study_permit)

def paid_leave(mod, p, d):
    return mod.x[p, d, 7] == mod.J[p, d]
model.paid_leave = py.Constraint(model.P, model.D, rule=paid_leave)

def _104_law(mod, p, d):
    return mod.x[p, d, 8] == mod.L[p, d]
model._104_law = py.Constraint(model.P, model.D, rule=_104_law)

def _1C_preassignment(mod, p, d):
    if mod.SO[p] == 1:
        return mod.x[p, d, 12] == mod.G[p, d]
    else:
        return py.Constraint.Skip
model._1C_preassignment = py.Constraint(model.P, model.D, rule=_1C_preassignment)

def _1A_preassignment(mod, p, d):
    if mod.SO[p] == 1:
        return mod.x[p, d, 9] == mod.E[p, d]
    else:
        return py.Constraint.Skip
model._1A_preassignment = py.Constraint(model.P, model.D, rule=_1A_preassignment)

def _2A_preassignment(mod, p, d):
    if mod.SO[p] == 1:
        return mod.x[p, d, 10] == mod.R[p, d]
    else:
        return py.Constraint.Skip
model._2A_preassignment = py.Constraint(model.P, model.D, rule=_2A_preassignment)

def _1B_preassignment(mod, p, d):
    if mod.SO[p] == 1:
        return mod.x[p, d, 11] == mod.U[p, d]
    else:
        return py.Constraint.Skip
model._1B_preassignment = py.Constraint(model.P, model.D, rule=_1B_preassignment)

def uniqueness_workshift(mod, p, d):
   return sum(mod.x[p, d, t] for t in mod.T) == 1
model.uniqueness_workshift = py.Constraint(model.P, model.D, rule=uniqueness_workshift)

def max_hours(mod, p):
   return mod.a >= mod.y[p]
model.max_hours = py.Constraint(model.P, rule=max_hours)

def calculate_sigma1(mod, p, d):
    if mod.SO[p] == 0:
        if d <= mod.d - 1:
            return sum(mod.x[p, l, 3] for l in range(d, d + 2)) >= 2 * mod.sigma[p, d]
        else:
            return py.Constraint.Skip
    else:
        return py.Constraint.Skip
model.calculate_sigma1 = py.Constraint(model.P, model.D, rule=calculate_sigma1)

def calculate_sigma2(mod, p, d):
    if mod.SO[p] == 0:
        if d <= mod.d - 1:
            return sum(mod.x[p, l, 3] for l in range(d, d + 2)) - 1 <= 2 * mod.sigma[p, d]
        else:
            return py.Constraint.Skip
    else:
        return py.Constraint.Skip
model.calculate_sigma2 = py.Constraint(model.P, model.D, rule=calculate_sigma2)

def calculate_gamma1(mod, p, d):
    if mod.SO[p] == 0:
        if d <= mod.d - 2:
            return sum(mod.x[p, l, 3] for l in range(d, d + 3)) >= 3 * mod.gamma[p, d]
        else:
            return py.Constraint.Skip
    else:
        return py.Constraint.Skip
model.calculate_gamma1 = py.Constraint(model.P, model.D, rule=calculate_gamma1)

def calculate_gamma2(mod, p, d):
    if mod.SO[p] == 0:
        if d <= mod.d - 2:
            return sum(mod.x[p, l, 3] for l in range(d, d + 3)) - 2 <= 3 * mod.gamma[p, d]
        else:
            return py.Constraint.Skip
    else:
        return py.Constraint.Skip
model.calculate_gamma2 = py.Constraint(model.P, model.D, rule=calculate_gamma2)

def triple_night_double_rest1(mod, p, d):
    if mod.SO[p] == 0:
        if d <= mod.d - 4:
            return 2 * mod.gamma[p, d] <= sum(mod.x[p, l, 4] for l in range(d + 3, d + 5))
        else:
            return py.Constraint.Skip
    else:
        return py.Constraint.Skip
model.triple_night_double_rest1 = py.Constraint(model.P, model.D, rule=triple_night_double_rest1)

def triple_night_double_rest2(mod, p, d):
    if mod.SO[p] == 0:
        if d <= mod.d - 3:
            return mod.gamma[p, d] <= mod.x[p, d + 3, 4]
        else:
            return py.Constraint.Skip
    else:
        return py.Constraint.Skip
model.triple_night_double_rest2 = py.Constraint(model.P, model.D, rule=triple_night_double_rest2)

def no_more_triple_consecutive_nights(mod, p, d):
    if mod.SO[p] == 0:
        if d > 3:
           return mod.x[p, (d - 3), 3] + mod.x[p, (d - 2), 3] + mod.x[p, (d - 1), 3] + mod.x[p, d, 3] <= 3
        else:
            return py.Constraint.Skip
    else:
        return py.Constraint.Skip
model.no_more_triple_consecutive_nights = py.Constraint(model.P, model.D, rule=no_more_triple_consecutive_nights)

def morning_shift_allowance(mod, p):
    if mod.SO[p] == 0:
        return sum(mod.x[p, d, 1] + mod.x[p, d, 9] for d in mod.D) >= mod.W[1] - mod.b[p, 1]
    else:
        return py.Constraint.Skip
model.morning_shift_allowance = py.Constraint(model.P, rule=morning_shift_allowance)

def afternoon_shift_allowance(mod, p):
    if mod.SO[p] == 0:
        return sum(mod.x[p, d, 2] + mod.x[p, d, 10] for d in mod.D) >= mod.W[2] - mod.b[p, 2]
    else:
        return py.Constraint.Skip
model.afternoon_shift_allowance = py.Constraint(model.P, rule=afternoon_shift_allowance)

def night_shift_allowance(mod, p):
    if mod.SO[p] == 0:
        return sum(mod.x[p, d, 3] for d in mod.D) >= mod.W[3] - mod.b[p, 3]
    else:
        return py.Constraint.Skip
model.night_shift_allowance = py.Constraint(model.P, rule=night_shift_allowance)

def feasibility_morning(mod, p):
    if mod.SO[p] == 0:
        return mod.b[p, 1] <= mod.W[1]
    else:
        return py.Constraint.Skip
model.feasibility_morning = py.Constraint(model.P, rule=feasibility_morning)

def feasibility_afternoon(mod, p):
    if mod.SO[p] == 0:
        return mod.b[p, 2] <= mod.W[2]
    else:
        return py.Constraint.Skip
model.feasibility_afternoon = py.Constraint(model.P, rule=feasibility_afternoon)

def feasibility_night(mod, p):
    if mod.SO[p] == 0:
        return mod.b[p, 3] <= mod.W[3]
    else:
        return py.Constraint.Skip
model.feasibility_night = py.Constraint(model.P, rule=feasibility_night)

def max_mornings_number(mod, p):
    if mod.SO[p] == 0:
        return mod.phi[1] >= sum(mod.x[p, d, 1] for d in mod.D)
    else:
        return py.Constraint.Skip
model.max_mornings_number = py.Constraint(model.P, rule=max_mornings_number)

def max_afternoons_number(mod, p):
    if mod.SO[p] == 0:
        return mod.phi[2] >= sum(mod.x[p, d, 2] for d in mod.D)
    else:
        return py.Constraint.Skip
model.max_afternoons_number = py.Constraint(model.P, rule=max_afternoons_number)

def max_nights_number(mod, p):
    if mod.SO[p] == 0:
        return mod.phi[3] >= sum(mod.x[p, d, 3] for d in mod.D)
    else:
        return py.Constraint.Skip
model.max_nights_number = py.Constraint(model.P, rule=max_nights_number)

def get_more_five_consecutive_working_days1(mod, p, d):
    if mod.SO[p] == 0:
        if d <= mod.d - 5:
            return sum(sum(mod.x[p, l, t] for t in range(1, 4)) for l in range(d, d + 6)) >= 6 * mod.k[p, d]
        else:
            return py.Constraint.Skip
    else:
        return py.Constraint.Skip
model.get_more_five_consecutive_working_days1 = py.Constraint(model.P, model.D, rule=get_more_five_consecutive_working_days1)

def get_more_five_consecutive_working_days2(mod, p, d):
    if mod.SO[p] == 0:
        if d <= mod.d - 5:
            return sum(sum(mod.x[p, l, t] for t in range(1, 4)) for l in range(d, d + 6)) - 5 <= 6 * mod.k[p, d]
        else:
            return py.Constraint.Skip
    else:
        return py.Constraint.Skip
model.get_more_five_consecutive_working_days2 = py.Constraint(model.P, model.D, rule=get_more_five_consecutive_working_days2)

def no_more_five_consecutive_working_days(mod, p, d):
    if mod.SO[p] == 0:
        return sum(sum(mod.k[p, d] for p in mod.P) for d in mod.D) == 0
    else:
        return py.Constraint.Skip
model.no_more_five_consecutive_working_days = py.Constraint(model.P, model.D, rule=no_more_five_consecutive_working_days)

def monthly_debt(mod, p):
    return mod.y[p] >= mod.wh * (1 - mod.SO[p])
model.monthly_debt = py.Constraint(model.P, rule=monthly_debt)

def total_holidays(mod, p):
    return sum(mod.x[p, d, 5] for d in mod.D) == mod.MH[p] + (mod.OH[p] - mod.mu[p])
model.total_holidays = py.Constraint(model.P, rule=total_holidays)

def feasibility_holidays(mod, p):
     return mod.mu[p] <= mod.OH[p]
model.feasibility_holidays = py.Constraint(model.P, rule=feasibility_holidays)

def operators_constraints1(mod, p, d):
    return mod.x[p, d, 1] + mod.x[p, d, 2] + mod.x[p, d, 3] <= (1 - mod.SO[p])
model.operators_constraints1 = py.Constraint(model.P, model.D, rule=operators_constraints1)

def operators_constraints2(mod, p, d):
    return mod.x[p, d, 9] + mod.x[p, d, 10] + mod.x[p, d, 11] + mod.x[p, d, 12] <= mod.SO[p]
model.operators_constraints2 = py.Constraint(model.P, model.D, rule=operators_constraints2)

# ottimizzazione
def minimize(dataDict, outfile, solverfile):
   assignment = {}
   hours = {}
   hours_per_workshifts = {}
   workshifts = {}
   instance = model.create_instance(dataDict)
   opt = py.SolverFactory(solver_name, executable=solver_path)
   opt.options['timelimit'] = 100
   start = time.time()
   opt.solve(instance, tee=True, logfile=solverfile)
   end = time.time()

   res = int(instance.obj_func.expr())

   # for p in instance.P:
   #     for d in instance.D:
   #         for t in instance.T:
   #              print("x_" + str(p) + str(d) + str(t) + ": " + str(instance.x[p, d, t].value))
   #     print("\n")

   for d in instance.D:
       for f in range(1, 4):
           if f == 1:
               workshifts[d, f] = 0
               for p in instance.P:
                   workshifts[d, f] += round(instance.x[p, d, 1].value) + round(instance.x[p, d, 9].value)
           if f == 2:
               workshifts[d, f] = 0
               for p in instance.P:
                   workshifts[d, f] += round(instance.x[p, d, 2].value) + round(instance.x[p, d, 10].value)
           if f == 3:
               workshifts[d, f] = 0
               for p in instance.P:
                   workshifts[d, f] += round(instance.x[p, d, 3].value)

   for p in instance.P:
       for d in instance.D:
           print("gamma " + str(p) + " - " + str(d) + ":" + str(instance.gamma[p, d].value))

   print()
   for p in instance.P:
       for d in instance.D:
           for t in instance.T:
               if round(instance.x[p, d, t].value) == 1:
                   if t == 1:
                       assignment[p, d] = 1
                       print(str(1) + str("  "), end='')
                   elif t == 2:
                       assignment[p, d] = 2
                       print(str(2) + str("  "), end='')
                   elif t == 3:
                       assignment[p, d] = 3
                       print(str(3) + str("  "), end='')
                   elif t == 4:
                       assignment[p, d] = 4
                       print(str("R ") + str(" "), end='')
                   elif t == 5:
                       assignment[p, d] = 5
                       print(str("F ") + str(" "), end='')
                   elif t == 6:
                       assignment[p, d] = 6
                       print(str("PS") + str(" "), end='')
                   elif t == 7:
                       assignment[p, d] = 7
                       print(str("PR") + str(" "), end='')
                   elif t == 8:
                       assignment[p, d] = 8
                       print(str("L ") + str(" "), end='')
                   elif t == 9:
                       assignment[p, d] = 9
                       print(str("1A") + str(" "), end='')
                   elif t == 10:
                       assignment[p, d] = 10
                       print(str("2A") + str(" "), end='')
                   elif t == 11:
                       assignment[p, d] = 11
                       print(str("1B") + str(" "), end='')
                   elif t == 12:
                       assignment[p, d] = 12
                       print(str("1C") + str(" "), end='')
       print()

   print()

   for p in instance.P:
       hours[p] = instance.y[p].value
       print(instance.y[p].value)

   print()

   for f in range(1, 4):
       for p in instance.P:
           sum = 0
           for t in instance.T:
               if f == 1:
                   if t == 1 or t == 9:
                       for d in instance.D:
                           sum += int(instance.x[p, d, t].value)
               if f == 2:
                   if t == 2 or t == 10:
                       for d in instance.D:
                           sum += int(instance.x[p, d, t].value)
               if f == 3:
                   if t == 3:
                       for d in instance.D:
                           sum += int(instance.x[p, d, t].value)
           print(sum)
           hours_per_workshifts[p, f] = sum
       print("\n")

   # searchPossibilePatterns(assignment, instance.P, instance.D)

   # file = open('file6.txt', 'w')
   # sys.stdout = file
   # instance.pprint()
   # file.close()
   return res, end - start
