# Cuckoo-Search-Algorithm
Python implementation of Cuckoo Search Algorithm
* Cuckoo Search Algoritmasi implement edilmis olup Xin-She Yang tarafindan yayimlanmis paper'dan yararlanilmistir.
* Kod calistirildiginda kullanicidan gerekli bilgileri acik bir sekilde istemektedir.(Populasyon dosyadan mi okunacak, rastgele mi olusturulacak? Parametreler neler? vb.)
* Parametrelerin aciklamasi su sekildedir:
	n =Populasyon nufusu, yani farkli yuvalarin(problemimiz icin cozumlerin) sayisi
	A = Cozumlerin her bileseninin alabilecegi minimum deger
	B = Cozumlerin her bileseninin alabilecegi maximum deger
	dimension = Cozumlerin kac bilesenden olusacagi(Kac boyutlu vektorler olacagi)
	iteration = Iterasyon sayisi
	pa = Gugukkusu yumurtalarinin kesfedilme orani 
* Program gerekli girdilerle calistirildiginda ekrana en iyi cozumu basmakta ve her iterasyonda buldugu en iyi cozumu gosteren bir grafik olusturmaktadir.
* Program bitiminde her adimdaki fitness ve en iyi cozumu txt dosyalarina yazdirmak icin 10-13 ve 85-88 satirlarindaki yorum kisimlarini yorum olmaktan cikariniz.
* Programa istediginiz fonksiyonu vermek icin 164. satiri degistiriniz.
