domains

city = string.
street = string.
house = integer.
flat = integer.

address = address(city, street, house, flat).
surname = string.
phone = integer.

model = string.
color = string.
price = integer.
serial = integer.

predicates

phone_record(surname, phone, address).
car(surname, model, color, price, serial).
fphs(serial, phone).
fscphmc(model, color, surname, phone, city).

clauses

phone_record(rich, 7777772, address(london, green, 1, 10)).
phone_record(rich, 7777771, address(london, green, 1, 10)).
phone_record(rich, 1111111, address(moscow, zelenaya, 2, 20)).
phone_record(middle, 9999999, address(moscow, ivanovskaya, 3, 2)).
phone_record(poor, 3333331, address(karaganda, pit, 23, 5)).
phone_record(poor, 3333332, address(perm, pit, 36, 7)).
phone_record(poor, 3333333, address(kop,leet, 2, 53)).

car(rich, coolmodel, red, 1000000, 123456).
car(rich, coolestmodel, green, 5000000, 837495).
car(rich, coolestmodel, blue, 5000000, 836472).
car(middle, awesommodel, red, 1000000, 047163).

fphs(Number, Phone) :- car(Surname, _, _, _, Number), phone_record(Surname, Phone, _).
fscphmc(CarModel, CarColor, Surname, Phone, City) :- car(Surname, CarModel, CarColor, _, _), phone_record(Surname, Phone, address(City, _, _, _)).

goal

  fscphmc(coolestmodel, green, Surname, Phone, City).