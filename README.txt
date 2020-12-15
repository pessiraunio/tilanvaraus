


- Lisätty room_listed ("huoneen julkaisu"), hakemalla huoneet näkyy kaikki huoneet
 koska tässä tapauksessa jwt_identityllä ei onnistu admin käyttäjän tunnistaminen
 mutta tiedoissa näkyy onko listed true vai false.

- Lisätty huoneen haku 

- Lisätty käyttäjän luonti

- Lisätty huoneen poistaminen vain adminille

- Lisätty huoneen luominen vain adminille

- Lisätty kirjautuminen, uloskirjautuminen, access token ja refresh token

- Lisätty huoneille description ja location, tällähetkellä huoneet voivat
 olla saman nimisiä koska "unique=True" ei toimi (?).

- ROOM idtä ei saa tällähetkellä nollattua (room id pysyy samana vaikka huoneita poistaa)

----14.12 - Pessi Raunio-----


- Varauksen poistaminen ei toimi tälllähtekellä. utf - 8 encoding ulinaa ...

----15.12 - Kaikki -----