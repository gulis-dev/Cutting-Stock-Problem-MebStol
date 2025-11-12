# Moje notatki z pracy nad algorytmem rozkroju

Mialem 6 formatek do pocięcia na płycie 100x100cm.

Zaczęło się prosto. Pomyślałem że wystarczy sortować formatki od największej i pchać je w najciaśniejsze wolne miejsce. Taka logika "Best Fit".

Ale od razu był pierwszy problem. Sortowanie po polu to był błąd. Program sam sobie zablokował płytę bo źle włożył formatkę B i przez to nie zmieściła się C. Zrobiłem więc inns atrategie ktora widzialem w internecie. Kazałem mu testować różne sortowania po polu po boku po wysokości i wybierać najlepsze.

No i zadziałało aż za dobrze. Znalazł układ 6/6. Tylko że... ten układ był okropny do cięcia. To był drugi problem i to dużo gorszy. Formatki były tak pozagnieżdżane że tworzyły cięcia w "L". Na pile nierealne.

Wtedy zrozumiałem. Prostota cięcia jest ważniejsza niż jakaś idealna oszczędność. Wyrzuciłem starą logikę podziału. Napisałem ją od zera. Nowa logika zawsze tworzy tylko czyste prostokąty. Żadnych "L".

Na koniec był jeszcze trzeci mały problem. Jak przeniosłem logikę do prostego skryptu to przestał działać. Okazało się że algorytm nie resetował płyty. Pierwsza strategia szła na czystej płycie a druga... na ścinkach po pierwszej. Bez sensu. Przeniosłem resetowanie stanu (list_of_vacancies = [sheet.copy()]) do środka pętli i każda strategia dostała nową płytę.

Po tym wszystkim mam w końcu algorytm który działa. Znajduje układ 6/6 i co najważniejsze da się to pociąć na pile.