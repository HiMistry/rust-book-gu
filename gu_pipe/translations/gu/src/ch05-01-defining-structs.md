## Defining and Instantiating Structs

રચનાઓ, "ટ્યૂપલ પ્રકાર" વિભાગમાં ચર્चित ટ્યૂપલ્સ જેવી જ છે, જેમાં બંને બહુવિધ સંબંધિત મૂલ્યો ધરાવે છે. ટ્યૂપલ્સની જેમ, રચનાના ભાગો પણ અલગ-અલગ પ્રકારના હોઈ શકે છે. પરંતુ ટ્યૂપલ્સથી વિપરીત, રચનામાં તમે દરેક ડેટા ભાગને નામ આપશો જેથી તે સ્પષ્ટ થાય કે મૂલ્યોનો અર્થ શું છે. આ નામો ઉમેરવાથી રચનાઓ ટ્યૂપલ્સ કરતાં વધુ લવચીક બને છે: તમારે ઉદાહરણની કિંમતોને નિર્દિષ્ટ કરવા અથવા ઍક્સેસ કરવા માટે ડેટાના ક્રમ પર આધાર રાખવાની જરૂર નથી.

To define a struct સ્ટ્રક્ચર (struct) વ્યાખ્યાયિત કરવા માટે, આપણે કીવર્ડ `struct` દાખલ કરીએ છીએ અને સમગ્ર સ્ટ્રક્ચરને નામ આપીએ છીએ. સ્ટ્રક્ચરનું નામ ડેટાના ટુકડાઓના મહત્વનું વર્ણન કરવું જોઈએ જે એકસાથે જૂથબદ્ધ કરવામાં આવે છે. ત્યારબાદ, કદાવલી બ્રેસ ({}) ની અંદર, આપણે ડેટા નામો અને પ્રકારો વ્યાખ્યાયિત કરીએ છીએ, જેને ફીલ્ડ (fields) કહેવામાં આવે છે. ઉદાહરણ તરીકે, યાદી 5-1 એક એવું સ્ટ્રક્ચર દર્શાવે છે જે user ખાતા વિશેની માહિતી સંગ્રહિત કરે છે.

<Listing number="5-1" file-name="src/main.rs" caption="A `User` struct definition">
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-01/src/main.rs:here}}
</Listing>
સ્ટ્રક્ચરનો ઉપયોગ કરવા માટે, આપણે તેને વ્યાખ્યાયિત કર્યા પછી, તેના ઉદાહરણ (instance) બનાવીએ છીએ, જેમાં દરેક ક્ષેત્રો માટે ચોક્કસ મૂલ્યો દર્શાવવામાં આવે છે. આપણે નામ અને પછી કુંડીક('{') ઉમેરીને ઉદાહરણ બનાવીએ છીએ, જેમાં `key: value` જોડીઓ હોય છે, જ્યાં કી એ ક્ષેત્રના નામ છે અને મૂલ્યો એ ડેટા છે જે આપણે તે ક્ષેત્રોમાં સંગ્રહ કરવા માંગીએ છીએ. આપણે સ્ટ્રક્ચરમાં જાહેર કરેલા ક્રમમાં જ ક્ષેત્રોનો ઉલ્લેખ કરવો જરૂરી નથી. બીજા શબ્દોમાં કહીએ તો, સ્ટ્રક્ચર વ્યાખ્યા પ્રકાર માટે એક સામાન્ય નકશો (template) જેવું છે, અને ઉદાહરણો તે નકશાને ચોક્કસ ડેટાથી ભરી દે છે જેથી કરીને પ્રકારના મૂલ્યો બનાવી શકાય. દાખલા તરીકે, આપણે યાદી 5-2 માં દર્શાવેલ પ્રમાણે કોઈ ચોક્કસ user જાહેર કરી શકીએ છીએ.

<Listing number="5-2" file-name="src/main.rs" caption="Creating an instance of the `User` struct">
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-02/src/main.rs:here}}
</Listing>
સ્ટ્રક્ચરમાંથી કોઈ ચોક્કસ મૂલ્ય મેળવવા માટે, અમે ડોટ સંકેતનો ઉપયોગ કરીએ છીએ. ઉદાહરણ તરીકે, આ userનું ઇમેઇલ સરનામું મેળવવા માટે, અમે `user1.email` નો ઉપયોગ કરીએ છીએ. જો ઇન્સ્ટન્સ પરિવર્તનશીલ હોય, તો અમે ડોટ સંકેતનો ઉપયોગ કરીને અને કોઈ ચોક્કસ ક્ષેત્રમાં મૂલ્ય સોંપીને તેને બદલી શકીએ છીએ. યાદી 5-3 દર્શાવે છે કે કેવી રીતે `User` ઇન્સ્ટન્સના પરિવર્તનશીલ `email` ક્ષેત્રનું મૂલ્ય બદલવું.

<Listing number="5-3" file-name="src/main.rs" caption="Changing the value in the `email` field of a `User` instance">
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-03/src/main.rs:here}}
</Listing>
એક નોંધ: સમગ્ર ઉદાહરણ સંશોધિત હોવું આવશ્યક છે; Rust આપણને માત્ર અમુક ક્ષેત્રોને સંશોધિત તરીકે ચિહ્નિત કરવાની મંજૂરી આપતું નથી. કોઈપણ અભિવ્યક્તિની જેમ, આપણે ફંક્શનના મુખ્ય ભાગમાં અંતિમ અભિવ્યક્તિ તરીકે structનું નવું ઉદાહરણ બનાવી શકીએ છીએ જેથી તે નવા ઉદાહરણને ગર્ભિત રીતે પરત

કરી શકાય. Listing 5-4 shows a `build_user` function that returns a `User` instance with the given email and username. The `active` field gets the value `true`, and the `sign_in_count` gets a value of `1`. લિસ્ટિંગ 5-4 એક `build_user` ફંક્શન દર્શાવે છે જે આપેલ ઇમેઇલ અને userનામ સાથે `User` ઉદાહરણ પરત કરે છે. `active` ક્ષેત્રને `true` મૂલ્ય મળે છે, અને `sign_in_count` ને `1` મૂલ્ય મળે છે.

<Listing number="5-4" file-name="src/main.rs" caption="A `build_user` function that takes an email and username and returns a `User` instance">
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-04/src/main.rs:here}}
</Listing>
તે કાર્ય પરિમાણોને સ્ટ્રક્ચર ક્ષેત્રોના નામ સમાન રાખવું યોગ્ય છે, પરંતુ `email` અને `username` ક્ષેત્ર નામો અને variable વારંવાર લખવું થોડું કંટાળાજનક છે. જો સ્ટ્રક્ચરમાં વધુ ક્ષેત્રો હોત, તો દરેક નામ વારંવાર લખવાથી વધુ હેરાન થવું પડત. નસીબમાં, એક અનુકૂળ સંક્ષિપ્ત રૂપ છે!

<!-- Old headings. Do not remove or links may break. -->
### Using the Field Init Shorthand

કારણ કે યાદી 5-4 માં પરિમાણ નામો અને struct ક્ષેત્ર નામો બરાબર સમાન છે, અમે ક્ષેત્ર પ્રારંભિક સંક્ષિપ્ત સિન્ટેક્સનો ઉપયોગ કરીને `build_user` ને ફરીથી લખી શકીએ છીએ જેથી તે બરાબર એ જ રીતે વર્તે પરંતુ તેમાં `username` અને `email` નું પુનરાવર્તન ન થાય, જે યાદી 5-5 માં દર્શાવેલ છે.

<Listing number="5-5" file-name="src/main.rs" caption="A `build_user` function that uses field init shorthand because the `username` and `email` parameters have the same name as struct fields">
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-05/src/main.rs:here}}
</Listing>
અહીં, આપણે `User` struct નો નવો ઉદ્દેશક બનાવી રહ્યા છીએ, જેમાં `email` નામનું ક્ષેત્ર છે. આપણે `email` ક્ષેત્રનું મૂલ્ય `build_user` વિધિના `email` પરિમાણ (parameter) માં રહેલા મૂલ્ય પર સેટ કરવા માંગીએ છીએ. કારણ કે `email` ક્ષેત્ર અને `email` પરિમાણ બંનેનું નામ એકસરખું છે, આપણે માત્ર `email` લખવાની જરૂર છે, `email: email` ને બદલે.

<!-- Old headings. Do not remove or links may break. -->
### Creating Instances with Struct Update Syntax

ઘણી વાર, structure નો નવો ઉદ્દેશ્ય બનાવવો ઉપયોગી થાય છે જેમાં અન્ય ઉદ્દેશ્યના મોટાભાગનાં મૂલ્યો હોય, પરંતુ તેમાં થોડા ફેરફાર કરવામાં આવે. તમે structure અપડેટ સિન્ટેક્સનો ઉપયોગ કરીને આ કરી શકો છો.

સૌ પ્રથમ, યાદી 5-6 માં અમે બતાવીએ છીએ કે નિયમિત રીતે `User` ઉદ્દેશ્ય કેવી રીતે બનાવવો, અપડેટ સિન્ટેક્સ વિના. અમે `email` માટે નવું મૂલ્ય સેટ કરીએ છીએ પરંતુ અન્યથા `user1` માંથી એ જ મૂલ્યોનો ઉપયોગ કરીએ છીએ જે我们在 યાદી 5-2 માં બનાવ્યા હતા.

<Listing number="5-6" file-name="src/main.rs" caption="Creating a new `User` instance using all but one of the values from `user1`">
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-06/src/main.rs:here}}
</Listing>
સ્ટ્રક્ચર અપડેટ સિન્ટેક્સનો ઉપયોગ કરીને, આપણે ઓછી કોડ સાથે સમાન પરિણામ મેળવી શકીએ છીએ, જે લિસ્ટિંગ 5-7 માં દર્શાવેલ છે. `..` સિન્ટેક્સ એ ઉલ્લેખિત નથી કે કયા ક્ષેત્રોને સ્પષ્ટ રીતે સેટ કરવામાં આવ્યા નથી, અને તેમને આપેલા ઇન્સ્ટન્સમાં ક્ષેત્રોના સમાન મૂલ્ય હોવું જોઈએ.

<Listing number="5-7" file-name="src/main.rs" caption="Using struct update syntax to set a new `email` value for a `User` instance but to use the rest of the values from `user1`">
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-07/src/main.rs:here}}
</Listing>
Listing 5-7 માં કોડ `user2` નું એક ઉદાહરણ પણ બનાવે છે જેમાં `email` માટે અલગ મૂલ્ય છે પરંતુ `username`, `active`, અને `sign_in_count` ક્ષેત્રોમાં `user1` જેવા જ મૂલ્યો છે. `..user1` અંતમાં આવવું જોઈએ જેથી અન્ય તમામ ક્ષેત્રોને `user1` ના અનુરૂપ ક્ષેત્રોમાંથી તેમના મૂલ્યો મળે, પરંતુ આપણે કોઈપણ ક્રમમાં ગમે તેટલા ક્ષેત્રો માટે મૂલ્ય સ્પષ્ટ કરવાનું પસંદ કરી શકીએ છીએ, struct ની વ્યાખ્યામાં ક્ષેત્રોના ક્રમને ધ્યાનમાં લીધા વિના.

નોંધ કરો કે સ્ટ્રક્ચર અપડેટ સિન્ટેક્સ `=` નો ઉપયોગ એસાઇનમેન્ટની જેમ કરે છે; આ એટલા માટે છે કારણ કે તે ડેટાને ખસેડે છે, બરાબર આપણે “ચલ અને ડેટા ક્રિયાપ્રતિક્રિયા સાથેનું મુવ” વિભાગમાં જોયું હતું. આ ઉદાહરણમાં, આપણે `user2` બનાવ્યા પછી `user1` નો ઉપયોગ કરી શકતા નથી કારણ કે `username` ક્ષેત્રમાં રહેલો `String` `user1` માંથી `user2` માં ખસેડવામાં આવ્યો છે. જો આપણે `email` અને `username` બંને માટે `user2` ને નવા `String` મૂલ્યો આપ્યા હોત, અને આમ માત્ર `active` અને `sign_in_count` મૂલ્યોનો ઉપયોગ `user1` માંથી કર્યો હોત, તો `user2` બનાવ્યા પછી પણ `user1` માન્ય રહેત. બંને `active` અને `sign_in_count` એવા પ્રકાર છે જે `Copy` ટ્રેઇટ લાગુ કરે છે, તેથી આપણે “માત્ર સ્ટેક ડેટા: કોપી” વિભાગમાં ચર્ચા કરી હતી તે વર્તન લાગુ થશે. આપણે આ ઉદાહરણમાં `user1.email` નો પણ ઉપયોગ કરી શકીએ છીએ, કારણ કે તેનું મૂલ્ય `user1` માંથી ખસેડવામાં આવ્યું ન હતું.

<!-- Old headings. Do not remove or links may break. -->
### Creating Different Types with Tuple Structs

Rust supports structures that resemble tuples, called tuple structures. Tuple structures have the added meaning provided by the structure name but do not have names associated with their fields; they only have the types of the fields. Tuple structures are useful when you want to give the entire tuple a name and make the tuple a different type from other tuples, and when naming each field as in a regular struct would be verbose or redundant.

ટ્યૂપલ સ્ટ્રક્ચર વ્યાખ્યાયિત કરવું ટ્યૂપલ સ્ટ્રક્ચર વ્યાખ્યાયિત કરવા માટે, `struct` કીવર્ડથી આરંભ કરો અને સ્ટ્રક્ચરના નામ પછી ટ્યૂપલમાં રહેલા પ્રકારો લખો. ઉદાહરણ તરીકે, અહીં આપણે બે ટ્યૂપલ સ્ટ્રક્ચર્સ વ્યાખ્યાયિત કરીએ છીએ અને તેનો ઉપયોગ કરીએ છીએ જેમના નામો `Color` અને `Point` છે:

<Listing file-name="src/main.rs">
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-01-tuple-structs/src/main.rs}}
</Listing>
નોંધ કરો કે `black` અને `origin` મૂલ્યો અલગ પ્રકારના છે કારણ કે તેઓ જુદા જુદા ટ્યૂપ સ્ટ્રક્ચર્સના ઉદાહરણો છે. તમે જે દરેક સ્ટ્રક્ચર વ્યાખ્યાયિત કરો છો તે પોતાનો પ્રકાર છે, ભલે સ્ટ્રક્ચરની અંદરના ક્ષેત્રો સમાન પ્રકારના હોય. દાખલા તરીકે, `Color` પ્રકારનું પરિમાણ લેતું ફંક્શન `Point` ને Argument તરીકે લઈ શકતું નથી, ભલે બંને પ્રકારો ત્રણ `i32` મૂલ્યોથી બનેલા હોય. અન્યથા, ટ્યૂપ સ્ટ્રક્ચર ઉદાહરણો ટ્યૂપ્લેસ જેવા જ છે જેમાં તમે તેમને તેમના વ્યક્તિગત ભાગોમાં તોડી શકો છો, અને તમે વ્યક્તિગત મૂલ્યને ઍક્સેસ કરવા માટે `.` ત્યારબાદ અનુક્રમણિકાનો ઉપયોગ કરી શકો છો. ટ્યૂપ્લેસથી વિપરીત, ટ્યૂપ સ્ટ્રક્ચર્સને તમે જ્યારે તોડો છો ત્યારે સ્ટ્રક્ચરના પ્રકારનું નામ આપવાની જરૂર પડે છે. ઉદાહરણ તરીકે, આપણે લખીશું `let Point(x, y, z) = origin;`  `origin` બિંદુમાં રહેલા મૂલ્યોને variables `x`, `y` અને `z` માં તોડવા માટે.

<!-- Old headings. Do not remove or links may break. -->
### Defining Unit-Like Structs

તમે એવા સ્ટ્રક્ચર્સ પણ વ્યાખ્યાયિત કરી શકો છો જેમાં કોઈ ક્ષેત્રો નથી! આને એકકીય-સમાન સ્ટ્રક્ચર્સ કહેવામાં આવે છે કારણ કે તે `()` જેવા એકકીય પ્રકારની જેમ વર્તે છે, જેનો ઉલ્લેખ આપણે “ધ ટ્યૂપલ ટાઈપ” વિભાગમાં કર્યો હતો. એકકીય-સમાન સ્ટ્રક્ચર્સ ઉપયોગી થઈ શકે છે જ્યારે તમારે કોઈ પ્રકાર પર trait લાગુ કરવાની જરૂર હોય પરંતુ તમારી પાસે એવો કોઈ ડેટા ન હોય જેને તમે જાતે જ પ્રકારમાં સંગ્રહ કરવા માંગો છો. આપણે પ્રકરણ ૧૦ માં traits વિશે ચર્ચા કરીશું. અહીં `AlwaysEqual` નામનાં એકકીય સ્ટ્રક્ચરને જાહેર (declare) અને ઉદ્ભવિત (instantiate) કરવાનું ઉદાહરણ છે:

<Listing file-name="src/main.rs">
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-04-unit-like-structs/src/main.rs}}
</Listing>
`AlwaysEqual` નિરૂપિત કરવા માટે, આપણે `struct` કીવર્ડનો ઉપયોગ કરીએ છીએ, ત્યારબાદ આપણે જે નામ આપવા માંગીએ છીએ અને પછી અર્ધવિરામચિહ્ન. કોઈ કળીબખોલ (curly brackets) અથવા કૌંસની જરૂર નથી! પછી, આપણે `subject` variable (variable) માં સમાન રીતે `AlwaysEqual` નો ઉદાહરણ મેળવી શકીએ છીએ: આપણે વ્યાખ્યાયિત કરેલા નામનો ઉપયોગ કરીને, કોઈપણ કળીબખોલ અથવા કૌંસ વિના. ધારો કે પાછળથી આપણે આ પ્રકાર માટે વર્તન લાગુ કરીશું જેથી `AlwaysEqual` નું દરેક ઉદાહરણ અન્ય કોઈપણ પ્રકારના દરેક ઉદાહરણ સમાન હોય, કદાચ પરીક્ષણ હેતુઓ માટે જાણીતા પરિણામ મેળવવા માટે. વર્તનને લાગુ કરવા માટે આપણને કોઈ ડેટાની જરૂર નથી! તમે પ્રકરણ ૧૦ માં જોશો કે કેવી રીતે લક્ષણો (traits) વ્યાખ્યાયિત કરવા અને કોઈપણ પ્રકાર પર તેનો અમલ કરવો, જેમાં એકમ-જેવા `struct` નો સમાવેશ થાય છે.

### સ્ટ્રક્ચર ડેટાની માલિકી

લિસ્ટિંગ 5-1 માં  `User`  સ્ટ્રક્ચર વ્યાખ્યામાં, અમે  `&str`  સ્ટ્રિંગ સ્લાઇસ પ્રકારને બદલે ઓન કરેલા  `String`  પ્રકારનો ઉપયોગ કર્યો છે. આ એક જાણીજોઈને કરેલો નિર્ણય છે કારણ કે અમે ઇચ્છીએ છીએ કે સ્ટ્રક્ચરમાં દરેક ઉદાહરણ તેની બધી માહિતીનું માલિકી ધરાવે અને તે માહિતી સ્ટ્રક્ચરના સમગ્ર જીવનકાળ સુધી માન્ય રહે.

સ્ટ્રક્ચર્સ અન્ય વસ્તુઓ દ્વારા માલિકી ધરાવતા ડેટાના સંદર્ભો સંગ્રહિત કરી શકે છે, પરંતુ આમ કરવા માટે  લાઇફટાઇમ્સ  ઉપયોગ કરવો જરૂરી છે, જે Rustની એક વિશેષતા છે કે જેના વિશે આપણે પ્રકરણ 10માં ચર્ચા કરીશું. લાઇફટાઇમ્સ સુનિશ્ચિત કરે છે કે સ્ટ્રક્ચર દ્વારા સંદર્ભિત ડેટા સ્ટ્રક્ચરના જીવનકાળ સુધી માન્ય રહે. ચાલો કહીએ કે તમે લાઇફટાઇમ સ્પષ્ટ કર્યા વિના સ્ટ્રક્ચરમાં સંદર્ભ સંગ્રહિત કરવાનો પ્રયાસ કરો છો, જેમ કે src/main.rs માં નીચે મુજબ; તો તે કામ કરશે નહીં:

<Listing file-name="src/main.rs">
<!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
struct User {
    active: bool,
    username: &str,
    email: &str,
    sign_in_count: u64,
}

fn main() {
    let user1 = User {
        active: true,
        username: "someusername123",
        email: "someone@example.com",
        sign_in_count: 1,
    };
}
</Listing>
સમ્પાઈલર જણાવશે કે તેને લાયફ્ટાઇમ સ્પેશિફાયર્સની જરૂર છે:

$ cargo run
   Compiling structs v0.1.0 (file:///projects/structs)
error[E0106]: missing lifetime specifier
 --> src/main.rs:3:15
  |
3 |     username: &str,
  |               ^ expected named lifetime parameter
  |
help: consider introducing a named lifetime parameter
  |
1 ~ struct User<'a> {
2 |     active: bool,
3 ~     username: &'a str,
  |

error[E0106]: missing lifetime specifier
 --> src/main.rs:4:12
  |
4 |     email: &str,
  |            ^ expected named lifetime parameter
  |
help: consider introducing a named lifetime parameter
  |
1 ~ struct User<'a> {
2 |     active: bool,
3 |     username: &str,
4 ~     email: &'a str,
  |

For more information about this error, try `rustc --explain E0106`.
error: could not compile `structs` (bin "structs") due to 2 previous errors
અપ્રમાણિત ભૂલોને સુધારવાની રીત વિશે આપણે પ્રકરણ ૧૦ માં ચર્ચા કરીશું જેથી તમે સ્ટ્રક્ચરમાં સંદર્ભો સંગ્રહિત કરી શકો, પરંતુ હાલમાં, આપણે `String` જેવા માલિકીવાળા પ્રકારોનો ઉપયોગ કરીને આ પ્રકારની ભૂલોને સુધારીશું, સંદર્ભો જેવા કે `&str` ને બદલે.

<!-- manual-regeneration
for the error above
after running update-rustc.sh:
pbcopy < listings/ch05-using-structs-to-structure-related-data/no-listing-02-reference-in-struct/output.txt
paste above
add `> ` before every line -->
