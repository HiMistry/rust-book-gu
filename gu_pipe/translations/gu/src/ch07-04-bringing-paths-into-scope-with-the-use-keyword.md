## Bringing Paths into Scope with the `use` Keyword

વિધેયોને બોલાવવા માટે માર્ગો લખવાની જરૂર પડવી એ અસુવિધાજનક અને પુનરાવર્તિત લાગી શકે છે. યાદી 7-7 માં, ભલે આપણે નિરપેક્ષ કે સાપેક્ષ માર્ગ પસંદ કર્યો હોય `add_to_waitlist` વિધેય માટે, દરેક વખતે જ્યારે આપણે `add_to_waitlist` બોલાવવા માંગતા હોઈએ, ત્યારે આપણે `front_of_house` અને `hosting` પણ સ્પષ્ટ કરવા પડ્યા. સદભાગ્યે, આ પ્રક્રિયાને સરળ બનાવવાનો એક માર્ગ છે: આપણે `use` કીવર્ડ વડે એકવાર માર્ગ માટે શોર્ટકટ બનાવી શકીએ છીએ અને પછી અવકાશમાં બીજે ક્યાંક ટૂંકા નામનો ઉપયોગ કરી શકીએ છીએ.

Listing 7-11 લિસ્ટિંગ 7-11 માં, અમે `crate::front_of_house::hosting` મોડ્યુલને `eat_at_restaurant` ફંક્શનના ક્ષેત્રમાં લાવીએ છીએ જેથી કરીને આપણે માત્ર `hosting::add_to_waitlist` ઉલ્લેખિત કરવું પડે, જે `eat_at_restaurant` માં `add_to_waitlist` ફંક્શનને બોલાવે.

<Listing number="7-11" file-name="src/lib.rs" caption="Bringing a module into scope with `use`">
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-11/src/lib.rs}}
</Listing>
Adding `use` and a path in a scope એક સ્કોપમાં `use` અને પાથ ઉમેરવું એ ફાઈલસિસ્ટમમાં સિમ્બોલિક લિંક બનાવવાની સમાન છે. `crate::front_of_house::hosting` ને ક્રેટ રૂટમાં ઉમેરવાથી, `hosting` તે સ્કોપમાં એક માન્ય નામ બને છે, જાણે કે `hosting` મોડ્યુલ ક્રેટ રૂટમાં વ્યાખ્યાયિત થયેલું હોય. `use` દ્વારા લાવવામાં આવેલા પાથ પણ અન્ય પાથની જેમ જ પ્રાઇવસી તપાસે છે.

નોંધ કરો કે `use` માત્ર તે ચોક્કસ સ્કોપ માટે શોર્ટકટ બનાવે છે જેમાં `use` આવેલું છે. લિસ્ટિંગ 7-12 `eat_at_restaurant` ફંક્શનને એક નવા ચાઈલ્ડ મોડ્યુલ `customer` માં ખસેડે છે, જે `use` વિધાન કરતાં અલગ સ્કોપ હોય છે, તેથી ફંક્શન બોડી કમ્પાઇલ થશે નહીં.

<Listing number="7-12" file-name="src/lib.rs" caption="A `use` statement only applies in the scope it’s in.">
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-12/src/lib.rs}}
</Listing>
કમ્પાઇલરની ભૂલ દર્શાવે છે કે આ ટૂંકા માર્ગ હવે `customer` મોડ્યુલમાં લાગુ પડતો નથી.

{{#include ../listings/ch07-managing-growing-projects/listing-07-12/output.txt}}
વર્તમાનમાં એક ચેતવણી પણ છે કે `use` હવે તેના કાર્યક્ષેત્રમાં વપરાતું નથી! આ સમસ્યાને સુધારવા માટે, `use` ને પણ `customer` મોડ્યુલમાં ખસેડો, અથવા બાળ `customer` મોડ્યુલમાં પિતૃ મોડ્યુલ સાથે `super::hosting` નો સંદર્ભ લો.

### Creating Idiomatic `use` Paths

યાદી 7-11 માં, તમે વિચારેલું હશે કે શા માટે અમે `use crate::front_of_house::hosting` ઉલ્લેખિત કર્યું અને પછી `eat_at_restaurant` માં `hosting::add_to_waitlist` ને બોલાવ્યું, તેના બદલે `use` માર્ગને સીધો `add_to_waitlist` કાર્ય સુધી લંબાવીને સમાન પરિણામ મેળવવું, જે યાદી 7-13 માં દર્શાવેલ છે.

<Listing number="7-13" file-name="src/lib.rs" caption="Bringing the `add_to_waitlist` function into scope with `use`, which is unidiomatic">
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-13/src/lib.rs}}
</Listing>
યાદ રાખો કે યાદી ૭-૧૧ અને યાદી ૭-૧૩ બંને સમાન કાર્ય પૂર્ણ કરે છે, પરંતુ યાદી ૭-૧૧ એ વિધેયને અવકાશમાં લાવવાનો રૂઢિચુસ્ત માર્ગ છે `use` સાથે. વિધેયના પિતૃ મોડ્યુલને અવકાશમાં લાવવાથી, આપણે વિધેયને બોલાવતી વખતે પિતૃ મોડ્યુલનો ઉલ્લેખ કરવો પડે છે. વિધેયને બોલાવતી વખતે પિતૃ મોડ્યુલનો ઉલ્લેખ કરવાથી સ્પષ્ટ થાય છે કે વિધેય સ્થાનિક રીતે વ્યાખ્યાયિત નથી, તેમ છતાં સંપૂર્ણ માર્ગનું પુનરાવર્તન ઓછું થાય છે. યાદી ૭-૧૩ માં રહેલો કોડ એ દર્શાવતો નથી કે `add_to_waitlist` ક્યાં વ્યાખ્યાયિત થયેલ છે.

બીજી બાજુ, જ્યારે struct, enum અને અન્ય વસ્તુઓને `use` સાથે લાવવામાં આવે છે, ત્યારે સંપૂર્ણ માર્ગ દર્શાવવો સામાન્ય છે. સૂચિ 7-14 બતાવે છે કે પ્રમાણભૂત લાયબ્રેરીના `HashMap` struct ને દ્વિસંગી crate ના કાર્યક્ષેત્રમાં લાવવાનો સામાન્ય અભિગમ.

<Listing number="7-14" file-name="src/main.rs" caption="Bringing `HashMap` into scope in an idiomatic way">
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-14/src/main.rs}}
</Listing>
અહીં આ રૂઢિ પાછળ કોઈ મજબૂત કારણ નથી: તે માત્ર એક સંમેલન છે જે ઉભરી આવ્યું છે, અને લોકોએ આ રીતે Rust કોડ વાંચવા અને લખવાની ટેવ પાડી

છે. આ રૂઢિનું અપવાદ એ છે કે જો આપણે `use` વિધાનો સાથે સમાન નામની બે વસ્તુઓ સ્કોપમાં લાવતા હોઈએ, કારણ કે Rust તે મંજૂરી આપતું નથી. સૂચિ 7-15 દર્શાવે છે કે કેવી રીતે સમાન નામ ધરાવતા પરંતુ અલગ મૂળ મોડ્યુલોના બે `Result` પ્રકારોને સ્કોપમાં લાવી શકાય છે, અને તેમનો ઉલ્લેખ કેવી રીતે કરવો.

<Listing number="7-15" file-name="src/lib.rs" caption="Bringing two types with the same name into the same scope requires using their parent modules.">
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-15/src/lib.rs:here}}
</Listing>
જેમ કે તમે જોઈ શકો છો, પિતૃ મોડ્યુલોનો ઉપયોગ બે `Result` પ્રકારોને અલગ પાડે છે. જો આપણે તેના બદલે `use std::fmt::Result` અને `use std::io::Result` ઉલ્લેખિત કર્યા હોત, તો આપણી પાસે સમાન ક્ષેત્રમાં બે `Result` પ્રકારો હોત, અને જ્યારે આપણે `Result` નો ઉપયોગ કર્યો હોત ત્યારે Rust ને ખબર ન પડતી કે આપણને કયો પ્રકાર જોઈએ છે.

### Providing New Names with the `as` Keyword

ઉપરોક્ત ઉકેલ ઉપરાંત, સમાન નામ ધરાવતા બે પ્રકારોને `use` દ્વારા એક જ અવકાશમાં લાવવાની અન્ય રીત એ છે કે પાથ પછી `as` અને પ્રકાર માટે નવું સ્થાનિક નામ અથવા ઉપનામ સ્પષ્ટ કરી શકાય. સૂચિ 7-16 દર્શાવે છે કે `as` નો ઉપયોગ કરીને બંને `Result` પ્રકારોમાંથી એકનું પુનર્નામકરણ કરીને સૂચિ 7-15 માં કોડને કેવી રીતે ફરીથી લખી શકાય.

<Listing number="7-16" file-name="src/lib.rs" caption="Renaming a type when it’s brought into scope with the `as` keyword">
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-16/src/lib.rs:here}}
</Listing>
બીજા `use` વિધાનમાં, અમે `std::io::Result` પ્રકાર માટે નવું નામ `IoResult` પસંદ કર્યું છે, જે `std::fmt` માંથી લાવવામાં આવેલા `Result` સાથે સંઘર્ષ કરશે નહીં. યાદી 7-15 અને યાદી 7-16ને રૂઢિચુસ્ત ગણવામાં આવે છે, તેથી પસંદગી તમારી ઉપર છે!

### Re-exporting Names with `pub use`

જ્યારે આપણે `use` કીવર્ડ વડે કોઈ નામ કાર્યક્ષેત્રમાં લાવીએ છીએ, ત્યારે તે નામ તે કાર્યક્ષેત્ર માટે ખાનગી રહે છે. તે કાર્યક્ષેત્રની બહારના કોડને પણ તે નામનો સંદર્ભ લેવાની મંજૂરી આપવા માટે, આપણે `pub` અને `use` ને જોડી શકીએ છીએ. આ તકનીકને ફરીથી નિકાસ (re-exporting) કહેવામાં આવે છે, કારણ કે આપણે એક વસ્તુને કાર્યક્ષેત્રમાં લાવી રહ્યા છીએ પરંતુ તે વસ્તુ અન્ય લોકો માટે પણ ઉપલબ્ધ કરાવતા પહેલાં.

સૂચિ 7-17 દર્શાવે છે કે સૂચિ 7-11 નો કોડ મૂળ મોડ્યુલમાં `use` ને બદલીને `pub use` કરવામાં આવ્યો છે.

<Listing number="7-17" file-name="src/lib.rs" caption="Making a name available for any code to use from a new scope with `pub use`">
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-17/src/lib.rs}}
</Listing>
આ પરિવર્તન પહેલાં, બાહ્ય કોડને `add_to_waitlist` વિધેયને પાથ `restaurant::front_of_house::hosting::add_to_waitlist()` દ્વારા બોલાવવું પડતું હતું, જેના માટે `front_of_house` મોડ્યુલને `pub` તરીકે ચિહ્નિત કરવું જરૂરી હતું. હવે કે આ `pub use` મૂળ મોડ્યુલમાંથી `hosting` મોડ્યુલને ફરીથી નિકાસ કરે છે, બાહ્ય કોડ પાથ `restaurant::hosting::add_to_waitlist()` નો ઉપયોગ કરી શકે છે. ફરીથી નિકાસ કરવું

એ ઉપયોગી છે જ્યારે તમારા કોડનું આંતરિક માળખું તમારા કોડને બોલાવતા પ્રોગ્રામરો દ્વારા ડોમેન વિશે વિચારવામાં આવતા માળખા કરતાં અલગ હોય છે. ઉદાહરણ તરીકે, આ રેસ્ટોરન્ટ રૂપક (metaphor) માં, રેસ્ટોરન્ટ ચલાવતા લોકો “ફ્રન્ટ ઓફ હાઉસ” અને “બેક ઓફ હાઉસ” વિશે વિચારે છે. પરંતુ રેસ્ટોરન્ટની મુલાકાત લેતા ગ્રાહકો સંભવિતપણે તે શબ્દોમાં ભાગો વિશે નહીં વિચારે. `pub use` સાથે, અમે એક માળખું લખી શકીએ છીએ પરંતુ અલગ માળખું બહાર લાવી શકીએ છીએ. આમ કરવાથી અમારી લાઇબ્રેરી લાઇબ્રેરી પર કામ કરતા પ્રોગ્રામરો અને લાઇબ્રેરીને બોલાવતા પ્રોગ્રામરો બંને માટે સારી રીતે સંગઠિત બને છે. અમે પ્રકરણ 14 માં “સુલભ જાહેર API ની નિકાસ” માં `pub use` નું બીજું ઉદાહરણ જોઈશું.

### Using External Packages

અગાઉના પ્રકરણ ૨ માં, આપણે એક અનુમાન લગાવવાની રમત પ્રોજેક્ટ બનાવ્યો હતો જેણે યાદ્ચ્છિક સંખ્યાઓ મેળવવા માટે `rand` નામના બાહ્ય પેકેજનો ઉપયોગ કર્યો હતો. `rand` ને આપણા પ્રોજેક્ટમાં વાપરવા માટે, આપણે આ લીટી Cargo.toml માં ઉમેરી હતી:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->
<Listing file-name="Cargo.toml">
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:9:}}
</Listing>
`Cargo.toml` માં `rand` ને આધાર તરીકે ઉમેરવાથી કાર્ગોને `rand` પેકેજ અને crates.io પરથી તેના આધારિત વસ્તુઓ ડાઉનલોડ કરવા અને આપણાં પ્રોજેક્ટ

માટે `rand` ઉપલબ્ધ કરાવવાનું કહેવામાં આવે છે. પછી, આપણાં પેકેજમાં `rand` ની વ્યાખ્યાઓને કાર્યક્ષેત્રમાં લાવવા માટે, આપણે `use` લાઇન ઉમેરી હતી જે ક્રેકેટના નામથી શરૂ થતી હતી, `rand`, અને જેમાં આપણે કાર્યક્ષેત્રમાં લાવવા માંગતા હતા તે વસ્તુઓની યાદી હતી. યાદ કરો કે પ્રકરણ ૨ માં “Generating a Random Number” માં, આપણે `Rng` ટ્રેઇટને કાર્યક્ષેત્રમાં લાવી હતી અને `rand::thread_rng` ફંક્શનને બોલાવ્યું હતું:

{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:ch07-04}}
સભ્યો Rust સમુદાયના સભ્યોએ ઘણાં પેકેજો crates.io પર ઉપલબ્ધ કરાવ્યા છે, અને તેમાંથી કોઈપણ પેકેજને તમારા પેકેજમાં સમાવવામાં આ જ પગલાંઓ સમાવિષ્ટ છે: તમારા પેકેજના Cargo.toml ફાઈલમાં તેમને સૂચિબદ્ધ કરવા અને `use` નો ઉપયોગ કરીને તેમના ક્રેટ્સમાંથી વસ્તુઓને અવકાશમાં લાવવી. નોંધ

કરો કે પ્રમાણભૂત `std` લાયબ્રેરી પણ એક ક્રેટ છે જે આપણા પેકેજની બહારનું છે. કારણ કે પ્રમાણભૂત લાયબ્રેરી Rust ભાષા સાથે જ આપવામાં આવે છે, તેથી આપણે Cargo.toml માં `std` ઉમેરવાની જરૂર નથી. પરંતુ આપણે તેનો ઉલ્લેખ `use` વડે કરવો પડશે જેથી કરીને ત્યાંથી વસ્તુઓને આપણા પેકેજના અવકાશમાં લાવી શકાય. દાખલા તરીકે, `HashMap` સાથે આપણે આ લીટીનો ઉપયોગ કરીશું:

use std::collections::HashMap;
આ એક સંપૂર્ણ માર્ગ છે જે `std` થી આરંભ થાય છે, પ્રમાણિત લાયબ્રેરી ક્રેટનું નામ.

<!-- Old headings. Do not remove or links may break. -->
### Using Nested Paths to Clean Up `use` Lists

જો આપણે એક જ crate અથવા એક જ module માં વ્યાખ્યાયિત કરેલા અનેક વસ્તુઓનો ઉપયોગ કરી રહ્યા હોય, તો દરેક વસ્તુને તેની પોતાની લીટી પર સૂચિબદ્ધ કરવાથી આપણી ફાઇલોમાં ઊભી જગ્યા ઘણી ખપાઈ શકે છે. ઉદાહરણ તરીકે, અનુક્રમણિકા 2-4 માં આપણે અનુમાન લગાવવાની રમતમાં રાખેલા આ બે `use` વિધાનો `std` માંથી વસ્તુઓને અવકાશમાં લાવે છે:

<Listing file-name="src/main.rs">
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-01-use-std-unnested/src/main.rs:here}}
</Listing>
અથવા, આપણે સંકલિત માર્ગોનો ઉપયોગ કરીને એક જ લીટીમાં સમાન વસ્તુઓને કાર્યક્ષેત્રમાં લાવી શકીએ છીએ. આ કરવા માટે, આપણે માર્ગના સામાન્ય ભાગને સ્પષ્ટ કરીએ છીએ, ત્યારબાદ બે કોલોન અને પછી કૌંસની અંદર ભાગોની યાદી આપીએ છીએ જે માર્ગોમાં ભિન્ન હોય છે, જે સૂચિ 7-18 માં દર્શાવેલ છે.

<Listing number="7-18" file-name="src/main.rs" caption="Specifying a nested path to bring multiple items with the same prefix into scope">
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-18/src/main.rs:here}}
</Listing>
`use` વિશાળ કાર્યક્રમોમાં, સમાન crate અથવા module માંથી અનેક વસ્તુઓને સ્કોપમાં

લાવવા માટે નેસ્ટેડ પાથનો ઉપયોગ કરવાથી જરૂરી અલગ `use` વિધાનની સંખ્યા ઘણી ઘટી શકે છે! આપણે નેસ્ટેડ પાથને પાથના કોઈપણ સ્તરે વાપરી શકીએ છીએ, જે બે `use` વિધાનોને જોડવા માટે ઉપયોગી છે જે સબપાથ વહેંચે છે. ઉદાહરણ તરીકે, યાદી 7-19 બે `use` વિધાનો દર્શાવે છે: એક જે `std::io` ને સ્કોપમાં લાવે છે અને બીજું જે `std::io::Write` ને સ્કોપમાં લાવે છે.

<Listing number="7-19" file-name="src/lib.rs" caption="Two `use` statements where one is a subpath of the other">
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-19/src/lib.rs}}
</Listing>
આ બે માર્ગોનો સામાન્ય ભાગ `std::io` છે, અને તે સંપૂર્ણ પ્રથમ માર્ગ છે. આ બે માર્ગોને એક `use` વિધાનમાં મર્જ કરવા માટે, આપણે નેસ્ટેડ માર્ગમાં `self` વાપરી શકીએ છીએ, જે યાદી 7-20 માં દર્શાવેલ છે.

<Listing number="7-20" file-name="src/lib.rs" caption="Combining the paths in Listing 7-19 into one `use` statement">
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-20/src/lib.rs}}
</Listing>
આ લીટી `std::io` અને `std::io::Write` ને કાર્યક્ષેત્રમાં લાવે છે.

<!-- Old headings. Do not remove or links may break. -->
### Importing Items with the Glob Operator

જો આપણે કોઈ પાથમાં વ્યાખ્યાયિત થયેલ તમામ જાહેર વસ્તુઓને અવકાશમાં લાવવા માંગતા હોઈએ, તો આપણે તે પાથને અનુસરીને `*` ગ્લોબ ઓપરેટરનો ઉલ્લેખ કરી શકીએ:

use std::collections::*;
આ `use` વિધાન `std::collections` માં વ્યાખ્યાયિત તમામ જાહેર વસ્તુઓને વર્તમાન અવકાશમાં લાવે છે. ગ્લોબ ઓપરેટરનો ઉપયોગ કરતી વખતે સાવચેત રહો! ગ્લોબથી કયા નામો અવકાશમાં છે અને તમારા કાર્યક્રમમાં વપરાયેલ નામ ક્યાં વ્યાખ્યાયિત કરવામાં આવ્યું હતું તે જાણવું મુશ્કેલ થઈ શકે છે. વધુમાં, જો આધાર રાખતી વસ્તુ તેની વ્યાખ્યાઓ બદલે છે, તો તમે જે આયાત કર્યું છે તે પણ બદલાય છે, જેના કારણે જ્યારે તમે આધાર રાખતી વસ્તુને અપગ્રેડ કરો છો ત્યારે કમ્પાઇલર ભૂલો આવી શકે છે, વિશેષ કરીને જો આધાર રાખતી વસ્તુ તમારા પોતાના અવકાશમાં સમાન નામની વ્યાખ્યા ઉમેરે તો.

ધાતુ સંકેતક ધાતુ સંકેતકનો ઉપયોગ પરીક્ષણો કરતી વખતે ઘણીવાર બધું જ પરીક્ષણ મોડ્યુલમાં લાવવા માટે થાય છે; આપણે તેના વિશે પ્રકરણ ૧૧ માં "પરીક્ષણો કેવી રીતે લખવા" માં વાત કરીશું. ધાતુ સંકેતકનો ઉપયોગ કેટલીક વાર પ્રસ્તાવના પેટર્નનો ભાગ રૂપે પણ થઈ શકે છે: તે પેટર્ન વિશે વધુ માહિતી માટે પ્રમાણિત લાયબ્રેરી દસ્તાવેજીકરણ જુઓ.

