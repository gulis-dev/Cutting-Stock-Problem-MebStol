Okej, miałem gotowy algorytm `main.py`. Czas przenieść to na Streamlit, żeby rekruter (i ojciec) mogli tego używać. Myślałem, że to będzie 20 minut roboty.

Pierwszy problem: tabela. Chciałem, żeby była interaktywna, więc użyłem `st.data_editor`. Ale nic nie działało. Za każdym razem, jak próbowałem coś wpisać w komórkę, tabela się resetowała do domyślnych wartości.

Straciłem na to chwilę. Okazało się, że Streamlit przeładowuje cały skrypt przy każdej pojedynczej akcji (np. kliknięciu). Logiczne. Musiałem przepisać logikę, żeby trzymał dane tabeli w `st.session_state`. Dopiero wtedy "zaskoczyło" i można było edytować dane.

Drugi problem: wizualizacja. Zdecydowałem się na `Matplotlib`, bo jest prosty. Ale on wywalił błąd `ValueError: Invalid RGBA argument`. Znowu, mój błąd. Skopiowałem format kolorów `rgba(R,G,B,A)` z webdev (Plotly), a Matplotlib tego nie rozumie. Oczekuje krotki z wartościami 0-1, np. `(0.9, 0.9, 0.9, 0.8)`.

Po poprawieniu kolorów, całość w końcu działała.

Samo wdrożenie na Streamlit Cloud to już było 15 minut roboty.

Wniosek: Znowu 80% czasu to walka z UI, stanem (`session_state`) i bibliotekami, a 20% to sam algorytm. Ale mam w końcu działający, publiczny link.