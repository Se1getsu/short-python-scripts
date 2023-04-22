# 【内容】
# 素数っぽい数を素因数分解付きで列挙します。

def eratosthenes_sieve(n):
    is_prime = [True]*(n + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, n + 1):
        if is_prime[p]:
            for q in range(2*p, n + 1, p):
                is_prime[q] = False
    return is_prime

def check(n):
	if ISP[n]: return False
	for p in (2,3,5):
		if n%p==0: return False
	return True

def factor(n):
    arr = []
    temp = n
    for i in range(2, int(-(-n**0.5//1))+1):
        if temp%i==0:
            cnt=0
            while temp%i==0:
                cnt+=1
                temp //= i
            arr.append([i, cnt])

    if temp!=1:
        arr.append([temp, 1])

    if arr==[]:
        arr.append([n, 1])

    return arr

def fact(n):
	ss = []
	for p,i in factor(n):
		ss.append('%s^%s' % (p,i) if i-1 else str(p))
	
	return ' * '.join(ss)



N = 300

ISP = eratosthenes_sieve(N)
for n in range(91,N):
	
	if check(n):
		print('%s\t= %s'%(n,fact(n)), end='\n')