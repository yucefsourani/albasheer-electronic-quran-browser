# مصحف البشير الالكتروني (مبني على مصحف عثمان الالكتروني) [English](#albasheer-electronic-quran-browser-based-on--othman-electronic-quran-browser)

<div align="center">

![logo](albasheer-128.png)

<h2><a href="https://arfedora.blogspot.com">فيدورا بالعربي</a></h2>

</div>

<div dir="rtl">


## رابط مشروع مصحف عثمان الالكتروني

https://github.com/ojuba-org/othman

## التغييرات مقابل مصحف عثمان

  1.  تحديث الى Python 3
  2.  اضافه دعم وضع الليلي مع خيار تفعيل
  3.  دعم تغيير لون الخلفيه واللون الايات
  4.  انشاء ملف windows EXE (pyinstaller/msys/mingw64)
  5.  اضافه خيار لاستخدام خط Amiri (ويندوز فقط)
  6.  دعم تلاوه من ملف MP3(من موقع ايات) و اضافه دعم التلاوه من ملفات ايات (*.ayt)
  7.  دعم التمرير التلقائي(scroll) مع التلاوه
  8.  دعم الترجمات من ايات و خيار اضافتها من ملفات ايات (*.ayt)
  9.  دعم التفاسير من ايار و خيار اضافتها من ملفات ايات (*.ayt)
  10. دعم تغيير سرعه التمرير التلقائي(scroll)
  11. دعم حفظ الصوره و الايه الحاليه عند اغلاق البرنامج
  12. بعض الاشياء الاخرى, مثل اضافه اختصارات
  
## الخطوات القادمة

 * محاوله دعم نظام الماك
 * اضافه امكانيه حفظ الاية
 * عمل حزمة RPM/مستودع Copr

## تنزيلات لويندوز (اذا كان لديك ويندوز 7 ولم يعمل البرنامج, تاكد من تحديث النظام)

### 32bit

https://github.com/yucefsourani/albasheer-electronic-quran-browser/releases/download/v1.0/albasheer32bit-setup.exe

### 64bit

https://github.com/yucefsourani/albasheer-electronic-quran-browser/releases/download/v1.0/albasheer64bit-setup.exe

## لينكس 

### فلات باك من Flathub

```
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo --user && flatpak install flathub com.github.yucefsourani.albasheer-electronic-quran-browser --user
```

### مباشرة

انسخ المستودع و قم بتشغيل albasheer-browser (يحتاج الى pygi و gstreamer(good و base) لتشغيل الايات من ملفات mp3 )

## الترخيص

مصحف البشير الالكتروني هو تحت رخصه **وقف** العامة الإصدار الأول من اعجوبه

https://ojuba.org/waqf:%D8%B1%D8%AE%D8%B5%D8%A9_%D9%88%D9%82%D9%81_%D8%A7%D9%84%D8%B9%D8%A7%D9%85%D8%A9

## الصور
![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot1.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot2.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot3.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot5.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot6.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot7.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot8.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot9.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot10.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot11.png "Screenshot")

</div>

# albasheer-electronic-quran-browser (based on  Othman Electronic Quran Browser)

https://arfedora.blogspot.com


## original Othman Electronic Quran Browser

https://github.com/ojuba-org/othman

## changelog 

  1.  Port To Python3
  2.  Add Switch To On/Off Dark Theme.
  3.  Support Change Background/Foreground Color.
  4.  Make Windows exe (pyinstaller/msys/mingw64)
  5.  Add Option To add Amiri Font (Windows Only).
  6.  support Audio Tilawa (mp3 from ayat) And add Option To add Audio tilawa from ayat files (*.ayt).
  7.  support Auto Scroll + Run Tilawa  .
  8.  support Tarajem (from ayat) And add Option To add Tajarem  from ayat files (*.ayt). 
  9.  support Tafasir (from ayat) And add Option To add Tafasir  from ayat files (*.ayt).
  10. support Speed Up/Down Auto scroll .
  11. support save/load last current sura aya.
  12. Other things like add some shortcuts and ...

## To Do 

 * trying support macOS .
 * add bookmark aya .
 * make rpm package/copr repository.

## Download For Windows (If Your system Windows 7 and albasheer fail to run update your system)

### 32bit

https://github.com/yucefsourani/albasheer-electronic-quran-browser/releases/download/v1.0/albasheer32bit-setup.exe


### 64bit

https://github.com/yucefsourani/albasheer-electronic-quran-browser/releases/download/v1.0/albasheer64bit-setup.exe


## Linux 

### flatpak from flathub

```
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo --user && flatpak install flathub com.github.yucefsourani.albasheer-electronic-quran-browser --user
```


### naitive

clone repository and run albasheer-browser (requires pygi and gstreamer(good and base)(to run mp3 tilawa))

## License

albasheer-electronic-quran-browser is under the "Waqf" General Public License from Ojuba

https://ojuba.org/waqf:license

## Screenshot
![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot1.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot2.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot3.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot5.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot6.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot7.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot8.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot9.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot10.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/albasheer-electronic-quran-browser/master/Screenshot11.png "Screenshot")




