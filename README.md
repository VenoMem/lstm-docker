
## Uruchamianie aplikacji Flask za pomocą Dockera

Nastąpiły zmiany, więc trzeba budować od nowa!
Aby uruchomić aplikację Flask za pomocą kontenera Docker, postępuj zgodnie z poniższymi krokami:

1. Zbuduj obraz Docker:

Przed uruchomieniem aplikacji, musisz zbudować obraz Docker na podstawie pliku Dockerfile.
`docker build -t nazwa_obrazu` .
Upewnij się, że znajdujesz się w katalogu, który zawiera plik Dockerfile. W miejsce nazwa_obrazu wpisz nazwę, którą chcesz przypisać obrazowi Docker.

2. Uruchom kontener Docker:

Po zbudowaniu obrazu Docker, możesz uruchomić kontener na podstawie tego obrazu.

`docker run nazwa_obrazu`


3. Uruchamiamy na
http://localhost:8080/

4. Jak chcemy zmienić port, bo np mamy już zajęty to:
`docker run -p 8080:8080 nazwa_obrazu`