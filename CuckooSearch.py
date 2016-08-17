from random import *
import numpy as np
from math import *
import matplotlib.pyplot as plt

class Cuckoo_Search():
    def __init__(self, n=25, A=1, B=10, dimension=15, iteration=3000, pa=0.25):
        # Sonuclari iceren .txt raporlarini olusturmak icin asagidaki dort satiri comment olmaktan cikarin.  
        '''
        with open("C:/Users/SİMLA/Desktop/fitness.txt", "w") as text_file:
            text_file.write("Her bir iterasyondaki fitness degeri:")
        with open("C:/Users/SİMLA/Desktop/results.txt", "w") as text_file:
            text_file.write("Algoritmanin ornek uzayda buldugu en iyi veri(bestnest) ve fonksiyondaki degeri(fmin): \n")
        '''
        # Kullanicidan populasyon ve parametreler hakkinda bilgi alinan kisim
        option=input("Populasyonu txt olarak vermek istiyorsaniz 1, program tarafindan olusturulmasini istiyorsaniz 2 giriniz: ")
        if(option=='1'):
            file=input("Dosyanin path'ini girin.")#C:/Users/SİMLA/Desktop/abc.txt
            with open(file, 'r') as f:
                data = [i.split(",") for i in f.read().split()]
                print(data)
            self.nests = np.array(data).astype('float')# text dosyasindaki populasyonu kodumuzda kullanabilecegimiz array tipine donusturur
            n=len(data)
            dimension=len(data[0])
            print("Lutfen belirtilen parametreleri giriniz:")
            A_in = input("A: ")
            A=float(A_in)
            B_in = input("B: ")
            B=float(B_in)
            iteration_in = input("iteration: ")
            iteration=int(iteration_in)
            pa_in = input("p_a: ")
            pa=float(pa_in)
        elif(option=='2'):
            print("Lutfen belirtilen sirayla parametreleri giriniz:")
            # Farkli yuvalarin/cozumlerin sayisi
            n_in = input("n: ")
            n=int(n)
            # Bir cozumdeki/yuvadaki bir bilesenin alabilecegi minimumu deger(lower bound)
            A_in = input("A: ")
            A=float(A_in)
            # Upper bound
            B_in = input("B: ")
            B=float(B_in)
            # Cozumlerin kac boyutlu vektorler oldugu
            dimension_in = input("dimension: ")
            dimension=int(dimension_in)
            # Iterasyon sayisi (Daha iyi sonuclar almak icin artirilmalidir.)
            iteration_in = input("iteration: ")
            iteration=int(iteration_in)
            # Gugukkusu yumurtalarinin kesfedilme orani
            pa_in = input("p_a: ")
            pa=float(pa_in)
            # Random olarak olusturulan ilk populasyon/cozum(solution) degerleri
            self.nests = np.array([[uniform(A, B) for k in range(dimension)] for i in range(n)])
        
        # Her bir cozum icin fonksiyondaki degerini bul
        self.fitness=(10**10)*np.ones(n)
        # Su anki en iyi cozumu al
        self.fmin,self.bestnest,self.nests,self.fitness=self.get_best_nest(self.nests,self.nests,self.fitness)
        # Her iterasyondaki en iyi cozumu tutan array(Grafik cizimi icin)
        arr=[]
        
        #Iterasyonlara basla
        self.count=0
        while(self.count<iteration):
            # Yeni cozumler uret, mevcut en iyiyi tut
            self.new_nest=self.get_cuckoos(self.nests,self.bestnest,A,B)
            self.fnew,self.best,self.nests,self.fitness=self.get_best_nest(self.nests,self.new_nest,self.fitness)
            # Sayaci guncelle
            self.count=self.count+n; 
            # Kesif ve randomization
            new_nest=self.empty_nests(self.nests,A,B,pa)
            # Su anki cozum kumelerindeki hesaplamalari yap
            self.fnew,self.best,self.nests,self.fitness=self.get_best_nest(self.nests,self.new_nest,self.fitness)
            # Sayaci guncelle
            self.count=self.count+n; 
            # Simdiye kadarki en iyi cozumu bul
            if self.fnew<self.fmin:
                self.fmin=self.fnew
                self.bestnest=self.best
            # Bu iterasyondaki en iyi cozumu array'e ekle
            arr.append(self.fmin)
        '''     
            with open("C:/Users/SİMLA/Desktop/fitness.txt", "a") as text_file:
                text_file.write("\n%s" % self.fitness)
        with open("C:/Users/SİMLA/Desktop/results.txt", "a") as text_file:
            text_file.write("bestnest: %s \nfmin: %s" % (self.bestnest,self.fmin))
        '''  
        # Her iterasyonda buldugu en iyi cozumu gosteren grafigi cizen kod parcasi
        plt.grid()
        x = np.array(arr)
        y=  np.array([k for k in range(int((iteration/(2*n))))])
        plt.plot(y, x, 'o-', color="r")
        plt.show()
        
        # En iyi cozumu ve fonksiyonda aldigi degeri ekrana yaz
        print("bestnest ", self.bestnest)
        print("fmin ", self.fmin)

    # Yeni sonuclar üreterek bazi yuvalari/cozumleri bunlarla degistir. pa olasilikla en kotu cozumler kesfedilip yenileriyle degistirilecek.
    def empty_nests(self,nest, A,B,pa):
        n=len(nest)
        dimension=len(nest[0])
        # Cozumun kesfedilip kesfedilmedigini tutan durum vektoru 
        K=np.array([np.random.random([len(nest),dimension])<pa],dtype=int)
        # Bir gugukkusunun yumurtasi eger ev sahibi yumurtaya cok benziyorsa o zaman kesfedilmesi dusuk bir olasiliktir.
        # Bu yuzden fitness cozumler arasindaki farkla iliskili olmali
        # Xin-She Yang'in belirttigi uzere boyle bir durumda random step size'lar ile biased/selective random walk yapmak mantikli olacaktir.
        stepsize=np.multiply(np.subtract(nest[np.random.permutation(n)],nest[np.random.permutation(n)]),np.multiply(.01,np.random.random())).copy()
        # Biased/selective random walk ile bulunmus yeni cozum
        new_nest=np.add(nest,np.multiply(stepsize,K[0])).copy()
        # Cozum degerlerinin alt ve ust sinirlarinin uygulanmasi(Rastgele uretildiginden siniri asmis olabilir)
        for i in range(n):
            for j in range(dimension):                   
                if new_nest[i][j]<A:
                    new_nest[i][j]=A
                if new_nest[i][j]>B:
                    new_nest[i][j]=B
        return new_nest
    
    # Random walk yaparak gugukkuslarini bul
    def get_cuckoos(self,nest,best,A,B):
        n=len(nest)
        dimension=len(nest[0])
        # Levy exponent ve Levy coefficient
        beta=3/2;
        sigma=(gamma(1+beta)*sin(pi*beta/2)/(gamma((1+beta)/2)*beta*2**((beta-1)/2)))**(1/beta)
        for i in range(len(nest)):
            s = nest[i]
            # Levy flight uygulamasinin basit bir yolu(Mantegna algoritmasi)
            u=np.multiply(np.random.randn(dimension),sigma)
            v=np.random.randn(dimension)
            step=np.divide(u,np.power(np.abs(v),np.divide(1.,beta)))
            # Eger cozum en iyi cozumse degistirme
            stepsize=np.multiply(.01,np.multiply(step,np.subtract(best,nest[i]))).copy()
            # Random walk
            s=(np.add(s,np.multiply(stepsize,np.random.randn(dimension))))[:]
            # Cozum degerlerinin alt ve ust sinirlarinin uygulanmasi(Rastgele uretildiginden siniri asmis olabilir)
            for j in range(dimension):                   
                if s[j]<A:
                    s[j]=A
                elif s[j]>B:
                    s[j]=B
            nest[i]=s.copy()
        return nest
    
    # Su anki en iyi cozumu bul
    def get_best_nest(self, nest,newnest,fitness):
        # Tum yeni cozumlerin fonksiyonda aldigi degerleri hesaplayip en iyilerle degistir
        for i in range(len(fitness)):
            fnew=self.f(newnest[i])
            if fnew<fitness[i]:
                fitness[i]=fnew
                nest[i]=newnest[i].copy()
        # En iyi cozumu ve indexini tut
        fmin=np.amin(fitness)
        index=np.argmin(fitness)
        best=nest[index]
        return (fmin,best,nest,fitness)
    
    # Objective Function(return'den sonraki kismi kendi fonksiyonunuzla degistirebilirsiniz.)
    def f(self,x):
        return sum([i**2 for i in x])        

a=Cuckoo_Search()