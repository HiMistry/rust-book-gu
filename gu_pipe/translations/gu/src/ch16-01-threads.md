## Using Threads to Run Code Simultaneously

મોટાભાગના વર્તમાન ઓપરેટિંગ સિસ્ટમ્સમાં, ચાલતા પ્રોગ્રામનો કોડ એક પ્રક્રિયા (process) માં ચાલે છે, અને ઓપરેટિંગ સિસ્ટમ એકસાથે બહુવિધ પ્રક્રિયાઓનું સંચાલન કરે છે. પ્રોગ્રામની અંદર, તમે સ્વતંત્ર ભાગો પણ રાખી શકો છો જે એકસાથે ચાલે છે. આ સ્વતંત્ર ભાગોને ચલાવવા માટેના લક્ષણોને થ્રેડ્સ (threads) કહેવામાં આવે છે. ઉદાહરણ તરીકે, વેબ સર્વર પાસે બહુવિધ થ્રેડ્સ હોઈ શકે છે જેથી તે એક જ સમયે એક કરતાં વધુ વિનંતીનો જવાબ આપી શકે.

તમારા પ્રોગ્રામમાં ગણતરીઓને બહુવિધ થ્રેડ્સમાં વિભાજીત કરીને બહુવિધ કાર્યોને એકસાથે ચલાવવાથી કાર્યક્ષમતા વધી શકે છે, પરંતુ તે જટિલતા પણ ઉમેરે છે. કારણ કે થ્રેડ્સ એકસાથે ચાલી શકે છે, તેથી અલગ-અલગ થ્રેડ્સ પર તમારા કોડના ભાગો કયા ક્રમમાં ચાલશે તેની કોઈ ખાતરી હોતી નથી. આનાં લીધે સમસ્યાઓ થઈ શકે છે, જેમ કે:

રેસ પરિસ્થિતિઓ, જેમાં થ્રેડો માહિતી અથવા સંસાધનોને અસંગત ક્રમમાં મેળવે છે

નિર્ણાયક સ્થિતિઓ, જેમાં બે થ્રેડો એકબીજાની રાહ જુએ છે, જેના કારણે બંને થ્રેડો આગળ વધી શકતા નથી

ભૂલો જે માત્ર અમુક ચોક્કસ પરિસ્થિતિઓમાં થાય છે અને તેને વિશ્વસનીય રીતે ફરીથી ઉત્પન્ન કરવી અને સુધારવી મુશ્કેલ છે

Rust પ્રયત્નો કરે છે કે થ્રેડ્સના ઉપયોગથી થતી નકારાત્મક અસરોને ઘટાડે, પરંતુ બહુથ્રેડીય સંદર્ભમાં પ્રોગ્રામિંગ કરવા માટે સાવચેતીપૂર્વક વિચાર કરવો જરૂરી છે અને તે એક જ થ્રેડમાં ચાલતા પ્રોગ્રામ કરતાં અલગ કોડ માળખું આવશ્યક છે. પ્રોગ્રામિંગ ભાષાઓ

થ્રેડ્સને અમુક અલગ રીતે લાગુ કરે છે, અને ઘણાં ઓપરેટિંગ સિસ્ટમ્સ પ્રોગ્રામિંગ ભાષાને નવા થ્રેડ બનાવવા માટે કૉલ કરી શકે તેવા API પ્રદાન કરે છે. Rust સ્ટાન્ડર્ડ લાયબ્રેરી થ્રેડના અમલીકરણનું 1:1 મોડેલ વાપરે છે, જેમાં પ્રોગ્રામ એક ઓપરેટિંગ સિસ્ટમ થ્રેડનો ઉપયોગ દરેક ભાષા થ્રેડ માટે કરે છે. એવા crates છે જે અન્ય મોડેલોના થ્રેડીંગને લાગુ કરે છે જે 1:1 મોડેલ સાથે જુદા જુદા વેપાર કરે છે. (Rustનું async સિસ્ટમ, જેને આપણે આગલા પ્રકરણમાં જોઈશું, તે પણ એકસાથે કાર્ય કરવાની બીજી રીત પ્રદાન કરે છે.)

### Creating a New Thread with `spawn`

નવું થ્રેડ બનાવવા માટે, આપણે `thread::spawn` ફંક્શનને બોલાવીએ છીએ અને તેને એક ક્લોઝર (આપણે પ્રકરણ ૧૩ માં ક્લોઝર વિશે વાત કરી હતી) પસાર કરીએ છીએ જેમાં આપણે નવા થ્રેડમાં ચલાવવા માંગીએ છીએ તે કોડ હોય છે. લિસ્ટિંગ ૧૬-૧ નું ઉદાહરણ મુખ્ય થ્રેડમાંથી થોડો ટેક્સ્ટ અને બીજા થ્રેડમાંથી થોડો ટેક્સ્ટ છાપે છે.

<Listing number="16-1" file-name="src/main.rs" caption="Creating a new thread to print one thing while the main thread prints something else">
```rust
```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-01/src/main.rs}}
```
```
</Listing>
નોંધ જ્યારે Rust કાર્યક્રમના મુખ્ય થ્રેડનું કાર્ય પૂર્ણ થાય છે, ત્યારે બનાવેલા તમામ થ્રેડો બંધ થઈ જાય છે, પછી ભલે તે ચાલુ હોય કે પૂર્ણ થયેલ હોય. આ કાર્યક્રમનું પરિણામ દરેક વખતે થોડું અલગ હોઈ શકે છે, પરંતુ તે નીચેના જેવું દેખાશે:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->
```text
```text
hi number 1 from the main thread!
hi number 1 from the spawned thread!
hi number 2 from the main thread!
hi number 2 from the spawned thread!
hi number 3 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the main thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
```
```
`thread::sleep` ના આહ્વાનો એક થ્રેડને થોડા સમય માટે તેના કાર્યને સ્થગિત કરવા દબાણ કરે છે, જેનાથી અન્ય થ્રેડ ચાલી શકે છે. સંભવતઃ થ્રેડો વારાફરતી ચાલશે, પરંતુ તેની ખાતરી નથી: તે તમારા ઓપરેટિંગ સિસ્ટમ થ્રેડોને કેવી રીતે સમય આપે તેના પર આધાર રાખે છે. આ કાર્યકાળમાં, મુખ્ય થ્રેડે પ્રથમ છાપ્યું, ભલે સ્પૉન થયેલ થ્રેડનું પ્રિન્ટ નિવેદન કોડમાં પહેલાં દેખાય. અને ભલે આપણે સ્પૉન થયેલા થ્રેડને `i` `9` થાય ત્યાં સુધી છાપવાનું કહ્યું હોય, તે મુખ્ય થ્રેડે બંધ કરી નાખ્યા પહેલાં માત્ર `5` સુધી જ પહોંચી શક્યો.

જો તમે આ કોડ ચલાવો અને માત્ર મુખ્ય થ્રેડનું પરિણામ જુઓ, અથવા કોઈ ઓવરલેપ ન જુઓ, તો થ્રેડો વચ્ચે સ્વિચ કરવા માટે ઓપરેટિંગ સિસ્ટમને વધુ તકો મળે તે માટે રેન્જમાંના આંકડા વધારવાનો પ્રયત્ન કરો.

<!-- Old headings. Do not remove or links may break. -->
### Waiting for All Threads to Finish

લિસ્ટિંગ ૧૬-૧ માં રહેલો કોડ મોટાભાગના સમયમાં થ્રેડને વહેલાસર બંધ કરી દે છે, કારણ કે મુખ્ય થ્રેડ સમાપ્ત થઈ જાય છે, અને થ્રેડો ચાલવાની ક્રમમાં કોઈ ચોક્કસતા ન હોવાથી, આપણે ખાતરીપૂર્વક કહી શકતા નથી કે સ્પોન થયેલ થ્રેડ ચાલે જશે!

આપણે `thread::spawn` નું રીટર્ન વેલ્યુ એક વેરિયેબલમાં સાચવીને સ્પોન થયેલ થ્રેડ ન ચાલવાની અથવા વહેલાસર સમાપ્ત થવાની સમસ્યાનું નિવારણ કરી શકીએ છીએ. `thread::spawn` નો રીટર્ન પ્રકાર `JoinHandle<T>` છે. `JoinHandle<T>` એ એક ઓન કરેલું વેલ્યુ છે, જેના પર આપણે `join` મેથડ કૉલ કરીએ ત્યારે તે તેના થ્રેડને પૂર્ણ થાય ત્યાં સુધી રાહ જુએ છીએ. લિસ્ટિંગ ૧૬-૨ દર્શાવે છે કે લિસ્ટિંગ ૧૬-૧ માં બનાવેલા થ્રેડના `JoinHandle<T>` નો ઉપયોગ કેવી રીતે કરવો અને `join` ને કૉલ કરીને `main` બહાર નીકળતા પહેલા સ્પોન થયેલ થ્રેડ પૂર્ણ થાય તેની ખાતરી કેવી રીતે કરવી.

<Listing number="16-2" file-name="src/main.rs" caption="Saving a `JoinHandle<T>` from `thread::spawn` to guarantee the thread is run to completion">
```rust
```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-02/src/main.rs}}
```
```
</Listing>
Calling `join` `join` ને બોલાવવાથી હેન્ડલ સાથે સંકળાયેલ થ્રેડ પૂર્ણ થાય ત્યાં સુધી વર્તમાન થ્રેડ અવરોધિત થઈ જાય છે. થ્રેડને અવરોધિત કરવાનો અર્થ એ થાય છે કે તે થ્રેડ કાર્ય કરવા અથવા બહાર નીકળતા અટકી જાય છે. આપણે `join` ને મુખ્ય થ્રેડના `for` લૂપ પછી મૂક્યું હોવાથી, યાદી 16-2 ચલાવવાથી આ પ્રકારનું પરિણામ ઉત્પન્ન થવું જોઈએ:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->
```text
```text
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 1 from the spawned thread!
hi number 3 from the main thread!
hi number 2 from the spawned thread!
hi number 4 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
```
```
બે થ્રેડ્સ આગળ ફેરવટ કરતા રહે છે, પરંતુ મુખ્ય થ્રેડ `handle.join()` ના આહ્વાનને કારણે રાહ જુએ છે અને ઉત્પન્ન થયેલ થ્રેડ પૂર્ણ ન થાય ત્યાં સુધી સમાપ્ત થતો નથી.

પરંતુ ચાલો જોઈએ કે જ્યારે આપણે `handle.join()` ને `main` માં `for` લૂપ પહેલાં ખસેડીએ ત્યારે શું થાય છે, આ પ્રમાણે:

<Listing file-name="src/main.rs">
```rust
```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/no-listing-01-join-too-early/src/main.rs}}
```
```
</Listing>
મુખ્ય થ્રેડ ઉત્પન્ન થયેલ થ્રેડ પૂર્ણ થાય ત્યાં સુધી રાહ જોશે અને પછી તેનું `for` લૂપ ચલાવશે, જેથી આઉટપુટ હવે ભળી નહિ જાય, જે અહીં દર્શાવેલ છે:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->
```text
```text
hi number 1 from the spawned thread!
hi number 2 from the spawned thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 3 from the main thread!
hi number 4 from the main thread!
```
```
નાની વિગતો, જેમ કે `join` ક્યાં બોલાવવામાં આવે છે, તે તમારા થ્રેડો એકસાથે ચાલે છે કે નહીં તેના પર અસર કરી શકે છે.

### Using `move` Closures with Threads

આપણે વારંવાર `thread::spawn` માં પાસ કરવામાં આવતા ક્લોઝર સાથે `move` કીવર્ડનો ઉપયોગ કરીએ છીએ કારણ કે તેનાથી ક્લોઝર userની પર્યાવરણમાંથી તે જે મૂલ્યો વાપરે છે તેનો હસ્તગતિકાર કરે છે, આમ તે મૂલ્યોનું માલિકી એક થ્રેડથી બીજા થ્રેડમાં સ્થાનાંતરિત થાય છે. પ્રકરણ ૧૩ માં "સંદર્ભો મેળવવું અથવા હસ્તગતિકાર કરવું" માં, આપણે ક્લોઝરના સંદર્ભમાં `move` વિશે ચર્ચા કરી હતી. હવે આપણે `move` અને `thread::spawn` વચ્ચેની ક્રિયાપ્રતિક્રિયા પર વધુ ધ્યાન કેન્દ્રિત કરીશું.

કૃતિ ૧૬-૧ માં નોંધ કરો કે આપણે `thread::spawn` માં પાસ કરેલો ક્લોઝર કોઈ Argumentો લેતો નથી: આપણે સ્પોન્ડ થ્રેડના કોડમાં મુખ્ય થ્રેડમાંથી કોઈ ડેટા વાપરતા નથી. સ્પોન્ડ થ્રેડમાં ડેટાનો ઉપયોગ કરવા માટે, સ્પોન્ડ થ્રેડના ક્લોઝરે તેને જરૂરી મૂલ્યો મેળવવા જોઈએ. યાદી ૧૬-૩ એક વેક્ટરને મુખ્ય થ્રેડમાં બનાવવાનો અને તેનો ઉપયોગ સ્પોન્ડ થ્રેડમાં કરવાનો પ્રયાસ દર્શાવે છે. જો કે, થોડીવાર પછી તમે જોશો કે તે કામ કરશે નહીં.

<Listing number="16-3" file-name="src/main.rs" caption="Attempting to use a vector created by the main thread in another thread">
```rust
```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-03/src/main.rs}}
```
```
</Listing>
ક્લોઝર `v` નો ઉપયોગ કરે છે, તેથી તે `v` ને કેપ્ચર કરશે અને તેને ક્લોઝરના પર્યાવરણનો ભાગ બનાવશે. કારણ કે `thread::spawn` આ ક્લોઝરને નવા થ્રેડમાં ચલાવે છે, આપણે `v` ને તે નવા થ્રેડની અંદરથી મેળવી શકીએ છીએ. પરંતુ જ્યારે આપણે આ ઉદાહરણને કમ્પાઇલ કરીએ છીએ, ત્યારે આપણને નીચેની ભૂલ મળે છે:

```console
```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-03/output.txt}}
```
```
Rust અનુમાન કરે છે કે `v` ને કેવી રીતે ગ્રહણ કરવું, અને કારણ કે `println!` ને માત્ર `v` ના સંદર્ભની જરૂર હોય છે, ક્લોઝર `v` ઉછીના લેવાનો પ્રયત્ન કરે છે. જોકે, એક સમસ્યા છે: Rust એ જણાવી શકતું નથી કે ઉત્પન્ન થયેલ થ્રેડ કેટલો સમય ચાલશે, તેથી તે જાણતું નથી કે `v` ના સંદર્ભ હંમેશાં માન્ય રહેશે કે નહીં.

ઉપશીષ્ટ ૧૬-૪ એક એવી પરિસ્થિતિ દર્શાવે છે જેમાં `v` નો સંદર્ભ અમાન્ય થવાની શક્યતા વધુ છે.

<Listing number="16-4" file-name="src/main.rs" caption="A thread with a closure that attempts to capture a reference to `v` from a main thread that drops `v`">
```rust
```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-04/src/main.rs}}
```
```
</Listing>
If Rust allowed us to run this code જો Rust આપણને આ કોડ ચલાવવા દેત, તો સંભવ છે કે શરૂ થયેલ થ્રેડ તરત જ પૃષ્ઠભૂમિમાં મૂકવામાં આવે અને બિલકુલ ચાલે નહીં. શરૂ થયેલ થ્રેડની અંદર `v` નો સંદર્ભ છે, પરંતુ મુખ્ય થ્રેડ તરત જ `v` ને છોડી દે છે, જે આપણે પ્રકરણ 15 માં ચર્ચા કરેલા `drop` ફંક્શનનો ઉપયોગ કરીને થાય છે. પછી, જ્યારે શરૂ થયેલ થ્રેડ અમલ કરવાનું શરૂ કરે છે, ત્યારે `v` હવે માન્ય નથી, તેથી તેનો સંદર્ભ પણ અમાન્ય છે. ઓહ

નો! Compiler ની ભૂલને સુધારવા માટે Listing 16-3 માં, આપણે ભૂલ સંદેશની સલાહનો ઉપયોગ કરી શકીએ છીએ:

<!-- manual-regeneration
after automatic regeneration, look at listings/ch16-fearless-concurrency/listing-16-03/output.txt and copy the relevant part
-->
```text
```text
help: to force the closure to take ownership of `v` (and any other referenced variables), use the `move` keyword
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++
```
```
`move` કીવર્ડનો ઉપયોગ ક્લોઝર પહેલાં કરવાથી, અમે ક્લોઝરને તે વાપરતા મૂલ્યોની માલિકી લેવાની ફરજ પાડીએ છીએ, તેના બદલે Rust ને અનુમાનિત કરવાની મંજૂરી આપીએ છીએ કે તેણે મૂલ્યો ઉછીના લેવા જોઈએ. લિસ્ટિંગ 16-3 માં કરેલો ફેરફાર લિસ્ટિંગ 16-5 માં દર્શાવ્યા મુજબ કમ્પાઇલ થશે અને આપણી ધાર્યા પ્રમાણે ચાલશે.

<Listing number="16-5" file-name="src/main.rs" caption="Using the `move` keyword to force a closure to take ownership of the values it uses">
```rust
```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-05/src/main.rs}}
```
```
</Listing>
આપણે એ જ વસ્તુ કરવાનો પ્રયત્ન કરવા પ્રેરાઈ શકીએ Listing 16-4 માં કોડ સુધારવા માટે જ્યાં મુખ્ય થ્રેડે `drop` ને `move` ક્લોઝર દ્વારા બોલાવ્યો હતો. જો કે, આ ઉપાય કામ નહીં કરે કારણ કે Listing 16-4 જે કરવાનો પ્રયત્ન કરી રહ્યું છે તે અન્ય કારણોસર પ્રતિબંધિત છે. જો આપણે ક્લોઝરમાં `move` ઉમેર્યું હોત, તો આપણે `v` ને ક્લોઝરના પર્યાવરણમાં ખસેડી શક્યા હોત, અને અમે મુખ્ય થ્રેડમાં તેના પર `drop` બોલાવી શક્યા ન હોત. તેના બદલે આપણને આ કમ્પાઇલર ભૂલ મળશે:

```console
```console
{{#include ../listings/ch16-fearless-concurrency/output-only-01-move-drop/output.txt}}
```
```
Rustની માલિકીના નિયમોએ ફરી એકવાર આપણને બચાવ્યા છે! Rust રૂઢિચુસ્ત રહીને માત્ર `v` ને મુખ્ય થ્રેડ માટે ઉછીના આપતું હોવાથી, યાદી 16-3 માં રહેલા કોડમાં આપણને ભૂલ મળી, જેના કારણે સ્પોન કરેલા થ્રેડનો સંદર્ભ (reference) સૈદ્ધાંતિક રીતે અમાન્ય થઈ શકે છે. `v` ની માલિકીને સ્પોન કરેલા થ્રેડને સોંપવા માટે Rust ને જણાવવાથી, અમે Rustને ખાતરી આપીએ છીએ કે મુખ્ય થ્રેડ હવે `v` નો ઉપયોગ કરશે નહીં. જો આપણે યાદી 16-4 માં પણ એ જ રીતે ફેરફાર કરીએ, તો જ્યારે આપણે મુખ્ય થ્રેડમાં `v` નો ઉપયોગ કરવાનો પ્રયાસ કરીએ ત્યારે આપણે માલિકીના નિયમોનું ઉલ્લંઘન કરીશું. `move` કીવર્ડ Rustની રૂઢિચુસ્ત ઉછીના લેવાની ડિફોલ્ટને વટાવી જાય છે; તે આપણને માલિકીના નિયમો તોડવા દેતું નથી.

હવે આપણે ધાઘાઓ શું છે અને થ્રેડ API દ્વારા પૂરા પાડવામાં આવેલ પદ્ધતિઓ વિશે વાત કરી લીધી છે, તો ચાલો કેટલાક એવા સંજોગો જોઈએ જેમાં આપણે ધાઘાઓનો ઉપયોગ કરી શકીએ છીએ.

