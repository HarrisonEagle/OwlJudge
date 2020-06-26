import math
a, b, h, m = map(int, input().split())

# aの時針が12時を0度にしたときに何度にあるか
# 時間分の角度 + 分針分の角度(60分で1/12度進むのでb分で何度進むかというとb*1/12 = 60 * x )
a_angle = h/12 + m*1/12/60
# 分針の角度
b_angle = m/60

# θはラジアン(円の半径に等しい長さの弧の中心に対する角度)である点に注意
# 要は360度 = 2*π
angle = abs(a_angle - b_angle)*2*math.pi

# 余弦定理より
# c^2 = a^2 + b^2 - 2*a*b*math.cos(angle)
print(math.sqrt(a*a + b*b - 2*a*b*math.cos(angle)))

# 別解それぞれの座標は以下の通りなので、座標間の距離を出しても良い
# a: (a*cos(a_angle),a*sin(a_angle)) b:(b*cos(b_angle),b*sin(b_angle))

#a_angle = a_angle * math.pi*2
#b_angle = b_angle * math.pi*2
#x1 = a*math.cos(a_angle)
#y1 = a*math.sin(a_angle)
#x2 = b*math.cos(b_angle)
#y2 = b*math.sin(b_angle)
#
#print(math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)))
