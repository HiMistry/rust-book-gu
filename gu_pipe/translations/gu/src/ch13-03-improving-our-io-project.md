## Improving Our I/O Project

આ પુનરાવર્તકો (iterators) વિશેની નવી જાણકારી સાથે, આપણે પ્રકરણ ૧૨ માંની I/O યોજનાને વધુ સ્પષ્ટ અને સંક્ષિપ્ત બનાવવા માટે પુનરાવર્તકોનો ઉપયોગ કરી શકીએ છીએ. ચાલો જોઈએ કે પુનરાવર્તકો `Config::build` વિધેય (function) અને `search` વિધેયના અમલીકરણમાં કેવી રીતે સુધારો કરી શકે છે.

### Removing a `clone` Using an Iterator

યાદી ૧૨-૬ માં, અમે કોડ ઉમેર્યો હતો જે `String` મૂલ્યોની સ્લાઈસ લીધી અને ઇન્ડેક્સિંગ દ્વારા `Config` સ્ટ્રક્ચરનું ઉદાહરણ બનાવ્યું હતું અને મૂલ્યોને ક્લોન કર્યા હતા, જેથી `Config` સ્ટ્રક્ચરે તે મૂલ્યોના માલિકી મેળવી શકે. યાદી ૧૩-૧૭ માં, અમે `Config::build` ફંક્શનનો અમલ ફરીથી પ્રસ્તુત કર્યો છે જે રીતે તે યાદી ૧૨-૨૩ માં હતો.

<Listing number="13-17" file-name="src/main.rs" caption="Reproduction of the `Config::build` function from Listing 12-23">
```rust
```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-23-reproduced/src/main.rs:ch13}}
```
```
</Listing>
`clone` તે સમયે, અમે કહ્યું હતું કે બિનકાર્યક્ષમ

`clone` કૉલ્સની ચિંતા ન કરવી, કારણ કે ભવિષ્યમાં તે દૂર કરી દેવામાં આવશે. સારું, તે સમય હવે આવી ગયો છે! અમને અહીં `clone` ની જરૂર હતી કારણ કે અમારી પાસે `String` તત્વો ધરાવતી સ્લાઇસ છે જે `args` પરિમાણમાં છે, પરંતુ `build` કાર્ય `args` નું માલિકી ધારણ કરતું નથી. `Config` ઇન્સ્ટન્સની માલિકી પાછી આપવા માટે, આપણે `query` અને `file_path` ક્ષેત્રોના મૂલ્યોને ક્લોન કરવા પડ્યા, જેથી `Config` ઇન્સ્ટન્સ તેના મૂલ્યોની માલિકી મેળવી શકે.

અમારા નવીન ઇટરેટર (iterator) વિશેના નવા જ્ઞાન સાથે, અમે `build` કાર્યને સ્લાઇસ (slice) ઉછીના લેવાને બદલે ઇટરેટરનું માલિકી સ્વીકારવાનું સુધારી શકીએ છીએ. અમે સ્લાઇસની લંબાઈ ચકાસી અને ચોક્કસ સ્થળોએ અનુક્રમણિકાનો ઉપયોગ કરેલા કોડને બદલે ઇટરેટર કાર્યક્ષમતાનો ઉપયોગ કરીશું. આ `Config::build` કાર્ય શું કરે છે તે સ્પષ્ટ કરશે કારણ કે ઇટરેટર મૂલ્યોને ઍક્સેસ કરશે. Once `Config::build` takes ownership of the iterator and stops using indexing operations that borrow, we

એકવાર `Config::build` ઇટરેટરની માલિકી સ્વીકારે અને ઉછીના લેવાની ક્રિયાઓનો ઉપયોગ કરવાનું બંધ કરે, પછી અમે ઇટરેટરથી `String` મૂલ્યોને `Config` માં ખસેડી શકીએ છીએ, ક્લોન (clone) બોલાવવા અને નવું ફાળવણી કરવાને બદલે.

#### Using the Returned Iterator Directly

તમારા I/O પ્રોજેક્ટની `src/main.rs` ફાઈલ ખોલો, જે આ પ્રમાણે દેખાતી હોવી જોઈએ:

ફાઈલનું નામ: src/main.rs

```rust
```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-24-reproduced/src/main.rs:ch13}}
```
```
અમે પ્રથમ `main` વિધેયની શરૂઆત બદલીશું જે આપણી પાસે લિસ્ટિંગ ૧૨-૨૪ માં હતી, તેને લિસ્ટિંગ ૧૩-૧૮ ના કોડમાં, જે આ વખતે એક પુનરાવર્તક (iterator) વાપરે છે. જ્યાં સુધી અમે `Config::build` ને પણ અપડેટ નહીં કરીએ ત્યાં સુધી આ કમ્પાઇલ થશે નહીં.

<Listing number="13-18" file-name="src/main.rs" caption="Passing the return value of `env::args` to `Config::build`">
```rust
```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-18/src/main.rs:here}}
```
```
</Listing>
The `env::args` Function `env::args` વિધેય એક iterator આપે છે! હવે આપણે iterator ના મૂલ્યોને vector માં ભેગા કરીને પછી `Config::build` ને slice મોકલવાને બદલે, સીધાં જ `env::args` દ્વારા મળેલા iterator નું ownership `Config::build` ને આપી રહ્યા છીએ.

આગળ, આપણે `Config::build` ની વ્યાખ્યા અપડેટ કરવાની જરૂર છે. ચાલો `Config::build` ના signature ને Listing 13-19 જેવું કરીએ. આ હજી સુધી compile થશે નહીં, કારણ કે આપણે function body ને અપડેટ કરવાની જરૂર છે.

<Listing number="13-19" file-name="src/main.rs" caption="Updating the signature of `Config::build` to expect an iterator">
```rust
```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-19/src/main.rs:here}}
```
```
</Listing>
The standard library documentation for the `env::args` function shows that the type of the iterator it returns is `std::env::Args`, and that type implements the `Iterator` trait and returns `String` values.

અમે `Config::build` ફંક્શનની નિશાનીને અપડેટ કર્યું છે જેથી પરિમાણ `args` પાસે સામાન્ય પ્રકાર (generic type) હોય, જેનાં લક્ષણો (trait bounds) `impl Iterator<Item = String>` છે, તેના બદલે `&[String]` હોય. આ `impl Trait` વાક્યરચનાનો ઉપયોગ અમે પ્રકરણ ૧૦ ના “Using Traits as Parameters” વિભાગમાં ચર્ચા કરી હતી, એનો અર્થ થાય છે કે `args` કોઈપણ પ્રકારનું હોઈ શકે છે જે `Iterator` લક્ષણો ધરાવે છે અને `String` વસ્તુઓ આપે છે.

કારણ કે અમે `args` નું માલિકી સ્વીકારી રહ્યા છીએ અને અમે તેના પર પુનરાવર્તન કરીને `args` ને બદલીશું, તેથી અમે `args` પરિમાણની વિશિષ્ટતામાં `mut` કીવર્ડ ઉમેરી શકીએ છીએ જેથી તે બદલી શકાય.

<!-- Old headings. Do not remove or links may break. -->
#### Using `Iterator` Trait Methods

આગળ, આપણે `Config::build` ના ભાગને સુધારીશું. કારણ કે `args` `Iterator` લક્ષણને અમલમાં મૂકે છે, આપણને ખબર છે કે આપણે તેના પર `next` પદ્ધતિને બોલાવી શકીએ છીએ! સૂચિ 13-20, સૂચિ 12-23 માંથી કોડને અપડેટ કરે છે જેથી `next` પદ્ધતિનો ઉપયોગ કરી શકાય.

<Listing number="13-20" file-name="src/main.rs" caption="Changing the body of `Config::build` to use iterator methods">
```rust
```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-20/src/main.rs:here}}
```
```
</Listing>
યાદ રાખો કે `env::args` ના પરિણામમાં પહેલું મૂલ્ય કાર્યક્રમનું નામ હોય છે. આપણે તેને અવગણવું અને આગળના મૂલ્ય પર જવું છે, તેથી પ્રથમ આપણે `next` ને બોલાવીએ છીએ અને વળતર મૂલ્ય સાથે કંઈક કરતા નથી. પછી, આપણે `query` ક્ષેત્રમાં મૂકવા માટે જોઈતું મૂલ્ય મેળવવા માટે `next` ને ફરીથી બોલાવીએ છીએ. જો `next` `Some` પરત કરે છે, તો આપણે મૂલ્ય કાઢવા માટે `match` નો ઉપયોગ કરીએ છીએ. જો તે `None` પરત કરે છે, તો તેનો અર્થ એ થાય છે કે પૂરતા Argumentો આપવામાં આવી નથી, અને આપણે વહેલા `Err` મૂલ્ય સાથે પાછા ફરો. આપણે `file_path` મૂલ્ય માટે પણ એ જ કરીએ છીએ.

<!-- Old headings. Do not remove or links may break. -->
### Clarifying Code with Iterator Adapters

આપણે `search` કાર્યમાં પણ ઇટરેટરનો લાભ લઈ શકીએ છીએ, જે આપણાં I/O પ્રોજેક્ટમાં છે, જે લિસ્ટિંગ 13-21 માં પુનઃપ્રoduction થયેલું છે, જેમ કે તે લિસ્ટિંગ 12-19 માં હતું.

<Listing number="13-21" file-name="src/lib.rs" caption="The implementation of the `search` function from Listing 12-19">
```rust
```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:ch13}}
```
```
</Listing>
આ કોડને પુનરાવર્તિત અનુરૂપ પદ્ધતિઓનો ઉપયોગ કરીને વધુ સંક્ષિપ્ત રીતે લખી શકાય છે. આમ કરવાથી આપણને પરિવર્તનશીલ મધ્યવર્તી `results` વેક્ટરની જરૂરિયાત ટાળવામાં પણ મદદ મળશે. કાર્યાત્મક પ્રોગ્રામિંગ શૈલી કોડને સ્પષ્ટ બનાવવા માટે પરિવર્તનશીલ સ્થિતિની માત્રા ઘટાડવાનું પસંદ કરે છે. પરિવર્તનશીલ સ્થિતિ દૂર કરવાથી ભવિષ્યમાં એક સુધારો શક્ય બની શકે છે, જેનાથી શોધ સમાંતર રીતે થઈ શકશે, કારણ કે આપણને `results` વેક્ટરની સમવર્તી ઍક્સેસનું સંચાલન કરવાની જરૂર નહીં પડે. સૂચિ 13-22 આ ફેરફાર દર્શાવે છે.

<Listing number="13-22" file-name="src/lib.rs" caption="Using iterator adapter methods in the implementation of the `search` function">
```rust
```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-22/src/lib.rs:here}}
```
```
</Listing>
યાદ રાખવું કે `search` વિધેયનો હેતુ `contents` માં રહેલી તમામ લીટીઓ પરત કરવાનો છે જેમાં `query` હોય છે. લિસ્ટિંગ ૧૩-૧૬ ના `filter` ઉદાહરણની જેમ, આ કોડ માત્ર એવાં લીટીઓને જ રાખવા માટે `filter` અનુકૂલનનો ઉપયોગ કરે છે જેના માટે `line.contains(query)` `true` પરત કરે છે. પછી આપણે મેળ ખાતી લીટીઓને બીજા વેક્ટર માં `collect` વડે એકત્રિત કરીએ છીએ. ઘણું સરળ! `search_case_insensitive` વિધેયમાં પણ પુનરાવર્તન પદ્ધતિઓનો ઉપયોગ કરવા માટે આ જ ફેરફાર કરવાની સ્વતંત્રતા રાખો.

વધુ સુધારણા માટે, `search` વિધેયમાંથી એક પુનરાવર્તક પરત કરો `collect` કૉલને દૂર કરીને અને પાછા ફરતો પ્રકાર `impl Iterator<Item = &'a str>` માં બદલીને જેથી વિધેય એક પુનરાવર્તક અનુકૂલન બને. નોંધ કરો કે તમારે પરીક્ષણોને પણ અપડેટ કરવાની જરૂર પડશે! તમારા `minigrep` સાધન વડે મોટી ફાઈલ શોધો આ ફેરફાર કરતા પહેલાં અને પછી વર્તનનો તફાવત જોવા માટે. આ ફેરફાર પહેલાં, પ્રોગ્રામ કોઈપણ પરિણામો છાપશે નહીં જ્યાં સુધી તે બધા પરિણામો એકત્રિત ન કરે, પરંતુ ફેરફાર પછી, પરિણામો દરેક મેળ ખાતી લીટી મળતાં જ છાપવામાં આવશે કારણ કે `run` વિધેયમાં `for` લૂપ પુનરાવર્તકની આળસનો લાભ લઈ શકે છે.

<!-- Old headings. Do not remove or links may break. -->
### Choosing Between Loops and Iterators

આગળ તાર્કિક પ્રશ્ન એ છે કે તમારે તમારી પોતાની કોડમાં કઈ શૈલી પસંદ કરવી જોઈએ અને શા માટે: લિસ્ટિંગ ૧૩-૨૧ માં મૂળ અમલીકરણ અથવા લિસ્ટિંગ ૧૩-૨૨ માં ઇટરેટર્સનો ઉપયોગ કરીને સંસ્કરણ (ધારી રહ્યા છીએ કે અમે પરિણામો બધી એકત્રિત કરીએ છીએ તે પહેલાં તેમને પરત કરતા નથી, તેના બદલે ઇટરેટરને પરત કરીએ છીએ). મોટા ભાગના Rust કાર્યકરો ઇટરેટર શૈલીનો ઉપયોગ કરવાનું પસંદ કરે છે. શરૂઆતમાં તેને સમજવામાં થોડું મુશ્કેલ લાગે છે, પરંતુ એકવાર તમને વિવિધ ઇટરેટર એડેપ્ટર્સ અને તેઓ શું કરે છે તેનો ખ્યાલ આવે, તો ઇટરેટર્સને સમજવા સરળ બની શકે છે. લૂપિંગના વિવિધ ભાગો સાથે ચેડાં કરવા અને નવા વેક્ટર્સ બનાવવાને બદલે, કોડ લૂપના ઉચ્ચ-સ્તરના ઉદ્દેશ્ય પર ધ્યાન કેન્દ્રિત કરે છે. આ સામાન્ય કોડને દૂર કરે છે જેથી કરીને આ કોડ માટે અનન્ય હોય તેવા ખ્યાલોને જોવાનું સરળ બને, જેમ કે ઇટરેટરની દરેક તત્વને પસાર થવું જોઈએ તે ફિલ્ટરિંગ શરત.

પરંતુ શું આ બે અમલીકરણો ખરેખર સમાન છે? સામાન્ય ધારણા એ હોઈ શકે છે કે નીચલા સ્તરનું `loop` વધુ ઝડપી હશે. ચાલો પ્રદર્શન વિશે વાત કરીએ.

