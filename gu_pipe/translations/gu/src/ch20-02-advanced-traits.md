## Advanced Traits

આપણે અગાઉ પ્રકરણ ૧૦ માં "લક્ષણો સાથે વર્તાયેલ વર્તણૂક વ્યાખ્યાયિત કરવી" વિભાગમાં લક્ષણો વિશે વાત કરી હતી, પરંતુ આપણે વધુ ઊંડા વિગતોની ચર્ચા કરી ન હતી. હવે જ્યારે તમને Rust વિશે વધુ ખબર છે, ત્યારે આપણે વિગતવાર બાબતો પર ધ્યાન કેન્દ્રિત કરી શકીએ છીએ.

<!-- Old headings. Do not remove or links may break. -->
### Defining Traits with Associated Types

સંબંધિત પ્રકારો (Associated types) એક પ્રકારના સ્થાને ચિહ્ન અને એક લક્ષણ (trait) ને જોડે છે, જેથી લક્ષણની પદ્ધતિ વ્યાખ્યાઓમાં આ સ્થાનાંતરિત પ્રકારોનો ઉપયોગ કરી શકાય. લક્ષણના અમલકર્તા (implementor) એ અમલીકરણ માટે વપરાયેલ નક્કર પ્રકારને સ્થાને ચિહ્ન પ્રકાર તરીકે સ્પષ્ટ કરશે. આ રીતે, આપણે એક લક્ષણ વ્યાખ્યાયિત કરી શકીએ છીએ જે કેટલાક પ્રકારોનો ઉપયોગ કરે છે પરંતુ તે પ્રકારો શું છે તે જાણવાની જરૂર નથી જ્યાં સુધી લક્ષણનું અમલીકરણ કરવામાં ન આવે.

આ પ્રકરણમાં વર્ણવેલ મોટાભાગની અદ્યતન વિશેષતાઓ ભાગ્યે જ જરૂરી હોય છે એમ કહ્યું છે. સંબંધિત પ્રકારો મધ્યમાં ક્યાંક છે: તેનો ઉપયોગ પુસ્તકની બાકીના ભાગમાં સમજાવવામાં આવેલા લક્ષણો કરતાં ઓછો થાય છે, પરંતુ આ પ્રકરણમાં ચર્ચા કરાયેલ અન્ય ઘણી વિશેષતાઓની તુલનામાં વધુ સામાન્ય રીતે થાય છે.

એક સંકળાયેલ પ્રકાર સાથેના લક્ષણનું ઉદાહરણ એક સંકળાયેલ પ્રકાર નામિત `Item` છે, જેનાં મૂલ્યોના પ્રકારને રજૂ કરે છે, જે પ્રકાર `Iterator` લક્ષણને અમલમાં મુકે છે. `Iterator` લક્ષણની વ્યાખ્યા યાદી 20-13 માં દર્શાવેલ છે.

<Listing number="20-13" caption="The definition of the `Iterator` trait that has an associated type `Item`">
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-13/src/lib.rs}}
</Listing>
The `Item` Type `Item` પ્રકાર એક અસ્થાયી સ્થાનાંતર છે, અને `next` પદ્ધતિની વ્યાખ્યા દર્શાવે છે કે તે `Option<Self::Item>` પ્રકારનાં મૂલ્યો પરત કરશે. `Iterator` લક્ષણના અમલીકરણકર્તાઓ `Item` માટે નક્કર પ્રકારનો ઉલ્લેખ કરશે, અને `next` પદ્ધતિ તે નક્કર પ્રકારના મૂલ્ય ધરાવતું `Option` પરત કરશે. સંબંધિત

પ્રકારો સામાન્ય રીતે જનરિક્સ જેવી જ લાગી શકે છે, જેમાં આપણે ફંક્શનને કયા પ્રકારનાં ડેટાને સંભાળી શકે છે તે નિર્દિષ્ટ કર્યા વિના વ્યાખ્યાયિત કરવાની મંજૂરી આપે છે. આ બે ખ્યાલો વચ્ચેનો તફાવત તપાસવા માટે, અમે `Counter` નામના પ્રકાર પર `Iterator` લક્ષણનું અમલીકરણ જોઈશું જે `Item` પ્રકારને `u32` તરીકે નિર્દિષ્ટ કરે છે:

<Listing file-name="src/lib.rs">
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-22-iterator-on-counter/src/lib.rs:ch19}}
</Listing>
આ સિન્ટેક્સ સામાન્ય રીતે જનરિક્સ (generics) જેવું લાગે છે. તો, શા માટે લિસ્ટિંગ ૨૦-૧૪ માં દર્શાવ્યા પ્રમાણે જનરિક્સ સાથે  `Iterator` ટ્રેઇટને વ્યાખ્યાયિત ન કરીએ?

<Listing number="20-14" caption="A hypothetical definition of the `Iterator` trait using generics">
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-14/src/lib.rs}}
</Listing>
The difference is that when using generics, as in Listing 20-14, we must annotate the types in each implementation; because we can also implement `Iterator<String>` for `Counter` or any other type, we could have multiple implementations of `Iterator` for `Counter`. In other words, when a trait has a generic parameter, it can be implemented for a type multiple times, changing the concrete types of the generic type parameters each time. When we use the `next` method on `Counter`, we would have to provide type annotations to indicate which implementation of `Iterator` we want to use.

સાથે સંકળાયેલ પ્રકારો સાથે, આપણને પ્રકારોની નોંધ કરવાની જરૂર નથી, કારણ કે આપણે એક જ પ્રકાર પર trait ને ઘણી વખત અમલમાં મૂકી શકતા નથી. લિસ્ટિંગ ૨૦-૧૩ માં, જે associée પ્રકારોનો ઉપયોગ કરીને વ્યાખ્યાયિત કરે છે, અમે `Item` ના પ્રકારને માત્ર એક જ વાર પસંદ કરી શકીએ છીએ કારણ કે ત્યાં માત્ર એક જ `impl Iterator for Counter` હોઈ શકે છે. આપણે સ્પષ્ટ કરવાની જરૂર નથી કે આપણે `Counter` પર `next` કૉલ કરીએ ત્યારે `u32` મૂલ્યોના iterator જોઈએ છીએ.

સાથે સંકળાયેલ પ્રકારો trait ના કરારનો પણ ભાગ બને છે: trait ના અમલીકરણકર્તાઓએ associée પ્રકારના placeholder માટે એક પ્રકાર પ્રદાન કરવો આવશ્યક છે. associée પ્રકારોમાં ઘણીવાર એવું નામ હોય છે જે વર્ણવે છે કે પ્રકારનો ઉપયોગ કેવી રીતે કરવામાં આવશે, અને API દસ્તાવેજીકરણમાં associée પ્રકારનું દસ્તાવેજીકરણ કરવી એ સારી પ્રથા છે.

<!-- Old headings. Do not remove or links may break. -->
### Using Default Generic Parameters and Operator Overloading

જ્યારે આપણે સામાન્ય પ્રકારના પરિમાણોનો ઉપયોગ કરીએ છીએ, ત્યારે આપણે સામાન્ય પ્રકાર માટે એક ડિફોલ્ટ નક્કર પ્રકાર સ્પષ્ટ કરી શકીએ છીએ. આ trait ના અમલીકરણકર્તાઓને જો ડિફોલ્ટ પ્રકાર કામ કરે તો નક્કર પ્રકાર સ્પષ્ટ કરવાની જરૂરિયાત દૂર કરે છે. તમે `<PlaceholderType=ConcreteType>` સિન્ટેક્સ સાથે સામાન્ય પ્રકાર જાહેર કરતી વખતે ડિફોલ્ટ પ્રકાર સ્પષ્ટ કરો છો.

આ તકનીક ક્યારે ઉપયોગી છે તેનું એક ઉત્તમ ઉદાહરણ ઓપરેટર ઓવરલોડિંગ (operator overloading) સાથેની પરિસ્થિતિ છે, જેમાં તમે ચોક્કસ પરિસ્થિતિઓમાં ઓપરેટર (જેમ કે `+`) નું વર્તન કસ્ટમાઇઝ કરો છો.

Rust તમને પોતાના ઓપરેટર બનાવવાની કે કોઈપણ અનિશ્ચિત ઓપરેટરને વધારે પડતા ભાર આપવાની અનુમતિ આપતું નથી. પરંતુ તમે `std::ops` માં દર્શાવેલ ક્રિયાઓ અને અનુરૂપ traits ને અમલમાં મૂકીને વધારે ભાર આપી શકો છો. ઉદાહરણ તરીકે, યાદી 20-15 માં, અમે બે `Point` ઇન્સ્ટન્સને એકસાથે ઉમેરવા માટે `+` ઓપરેટરને વધારે ભાર આપીએ છીએ. અમે આ `Point` struct પર `Add` trait ને અમલમાં મૂકીને કરીએ છીએ.

<Listing number="20-15" file-name="src/main.rs" caption="Implementing the `Add` trait to overload the `+` operator for `Point` instances">
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-15/src/main.rs}}
</Listing>
The `add` Method `add` પદ્ધતિ બે `Point` સંસ્થાઓના `x` મૂલ્યો અને બે `Point` સંસ્થાઓના `y` મૂલ્યો ઉમેરીને એક નવી `Point` બનાવે છે. `Add` લક્ષણનો એક સાંકળિત પ્રકાર નામ `Output` છે, જે `add` પદ્ધતિમાંથી પાછો મળતો પ્રકાર નક્કી કરે

છે. આ કોડમાં ડિફૉલ્ટ સામાન્ય પ્રકાર `Add` લક્ષણમાં રહેલો છે. અહીં તેની વ્યાખ્યા છે:

trait Add<Rhs=Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
આ કોડ સામાન્ય રીતે પરિચિત દેખાશે: એક trait જેમાં એક method અને સંકળાયેલ type છે. નવું ભાગ `Rhs=Self` છે: આ syntax ને default type parameters કહેવામાં આવે છે. `Rhs` generic type parameter (જે “right-hand side” માટે ટૂંકું નામ છે) એ `add` method માં `rhs` પરિમાણનો type વ્યાખ્યાયિત કરે છે. જો આપણે `Add` trait ના અમલીકરણ વખતે `Rhs` માટે કોઈ ચોક્કસ type નો ઉલ્લેખ ન કરીએ, તો `Rhs` નો type `Self` પર default થશે, જે એ type હશે જેના પર આપણે `Add` નો અમલ કરી રહ્યા છીએ.

જ્યારે આપણે `Point` માટે `Add` અમલમાં મૂક્યું, ત્યારે આપણે `Rhs` માટે ડિફોલ્ટનો ઉપયોગ કર્યો કારણ કે આપણે બે `Point` ઇન્સ્ટન્સ ઉમેરવા માંગતા હતા. ચાલો એક એવું ઉદાહરણ જોઈએ જ્યાં આપણે `Add` ટ્રેઇટને અમલમાં મૂકીએ છીએ જ્યાં આપણે ડિફોલ્ટનો ઉપયોગ કરવાને બદલે `Rhs` પ્રકારને કસ્ટમાઇઝ કરવા માંગીએ છીએ.

આપણી પાસે બે સ્ટ્રક્ચર્સ છે, `Millimeters` અને `Meters`, જે જુદા જુદા એકમોમાં મૂલ્યો ધરાવે છે. આ હાલના પ્રકારને બીજા સ્ટ્રક્ચરમાં પાતળું આવરણ આપવું એ ન્યૂટાઇપ પેટર્ન તરીકે ઓળખાય છે, જેને આપણે “Implementing External Traits with the Newtype Pattern” વિભાગમાં વધુ વિગતવાર વર્ણવવામાં આવ્યું છે. આપણે મિલીમીટરમાં મૂલ્યોને મીટરમાં મૂલ્યો સાથે ઉમેરવા માંગીએ છીએ અને `Add` નું અમલીકરણ યોગ્ય રીતે રૂપાંતરણ કરે તેવું ઇચ્છવું છે. આપણે `Millimeters` માટે `Meters` ને `Rhs` તરીકે `Add` નો અમલ કરી શકીએ છીએ, જે લિસ્ટિંગ 20-16 માં દર્શાવેલ છે.

<Listing number="20-16" file-name="src/lib.rs" caption="Implementing the `Add` trait on `Millimeters` to add `Millimeters` and `Meters`">
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-16/src/lib.rs}}
</Listing>
એકમોમાં `મિલીમીટર` અને `મીટર` ઉમેરવા માટે, આપણે `impl Add<Meters>` સ્પષ્ટ કરીએ છીએ જેથી `Rhs` પ્રકારના પરિમાણનું મૂલ્ય `Self` ની બદલે સેટ થાય.

તમે બે મુખ્ય રીતે ડિફોલ્ટ પ્રકારના પરિમાણોનો ઉપયોગ કરશો:

હાલના કોડને તોડ્યા વિના એક પ્રકારને વિસ્તારવા માટે,

અને ચોક્કસ કિસ્સાઓમાં કસ્ટમાઇઝેશન કરવાની મંજૂરી આપવા માટે જેમાં મોટાભાગના userઓને જરૂર નહીં હોય.

સ્ટાન્ડર્ડ લાયબ્રેરીનું `Add` ટ્રેઇટ બીજા હેતુનું ઉદાહરણ છે: સામાન્ય રીતે, તમે બે સમાન પ્રકારો ઉમેરશો, પરંતુ `Add` ટ્રેઇટ તમને તેની બહાર પણ કસ્ટમાઇઝ કરવાની ક્ષમતા પૂરી પાડે છે. `Add` ટ્રેઇટની વ્યાખ્યામાં ડિફોલ્ટ પ્રકાર પરિમાણનો ઉપયોગ કરવાથી તમારે મોટાભાગના સમય વધારાના પરિમાણને સ્પષ્ટ કરવાની જરૂર નથી રહેતી. બીજા શબ્દોમાં કહીએ તો, અમલીકરણનું થોડું બોઇલરપ્લેટ જરૂરી નથી, જેનાથી ટ્રેઇટનો ઉપયોગ કરવો સરળ

બને છે. The first purpose is similar to the second but in reverse: If you want to add a type parameter to an existing trait, you can give it a default to allow extension of the functionality of the trait without breaking the existing implementation code. પહેલો હેતુ બીજા જેવો જ છે પરંતુ વિરુદ્ધ છે: જો તમે કોઈ હાલના ટ્રેઇટમાં પ્રકાર પરિમાણ ઉમેરવા માંગતા હો, તો તમે તેને ડિફોલ્ટ આપી શકો છો જેથી ટ્રેઇટની કાર્યક્ષમતાને હાલના અમલીકરણ કોડને તોડ્યા વિના વધારી શકાય.

<!-- Old headings. Do not remove or links may break. -->
### Disambiguating Between Identically Named Methods

Rust માં એવું કશું નથી જે કોઈ trait માં બીજા trait ના વિધિ જેટલું જ નામ ધરાવતું વિધિ હોવા અટકાવે, ન તો Rust તમને એક જ type પર બંને traits ને અમલમાં મૂકતા અટકાવે છે. એ જ રીતે, type પર સીધું જ વિધિ અમલમાં મૂકવું પણ શક્ય છે જે traits ના વિધિઓ જેટલું નામ ધરાવે છે.

સમાન નામનાં વિધિઓને બોલાવતી વખતે, તમારે Rust ને કયું વાપરવું છે તે જણાવવું પડશે. Listing 20-17 માં આપેલા કોડને ધ્યાનમાં લો જ્યાં આપણે બે traits, `Pilot` અને `Wizard`, વ્યાખ્યાયિત કર્યા છે, જેમાં બંને પાસે `fly` નામનું વિધિ છે. પછી આપણે `Human` type પર બંને traits ને અમલમાં મૂકીએ છીએ, જે પહેલાથી જ `fly` નામનું વિધિ ધરાવે છે. દરેક `fly` વિધિ કંઈક અલગ કરે છે.

<Listing number="20-17" file-name="src/main.rs" caption="Two traits are defined to have a `fly` method and are implemented on the `Human` type, and a `fly` method is implemented on `Human` directly.">
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-17/src/main.rs:here}}
</Listing>
જ્યારે આપણે `Human` ના ઉદાહરણ પર `fly` ને બોલાવીએ છીએ, ત્યારે કમ્પાઇલર આપોઆપ જ તે પદ્ધતિને બોલાવે છે જે પ્રકાર પર સીધી રીતે અમલમાં મુકાયેલી છે, જે યાદી ૨૦-૧૮ માં દર્શાવેલ છે.

<Listing number="20-18" file-name="src/main.rs" caption="Calling `fly` on an instance of `Human`">
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-18/src/main.rs:here}}
</Listing>
આ કોડ ચલાવવાથી `*હાથ જોરથી હલાવતા*` પ્રિન્ટ થશે, જે દર્શાવે છે કે Rust એ `Human` પર અમલમાં મૂકેલી `fly` પદ્ધતિને સીધી

રીતે બોલાવી. `Pilot` અથવા `Wizard` લક્ષણોમાંથી `fly` પદ્ધતિઓને બોલાવવા માટે, આપણે વધુ સ્પષ્ટ વાક્યરચનાનો ઉપયોગ કરવો પડશે જે દર્શાવે છે કે આપણે કઈ `fly` પદ્ધતિનો ઉલ્લેખ કરીએ છીએ. સૂચિ 20-19 આ વાક્યરચનાનું નિદર્શન કરે છે.

<Listing number="20-19" file-name="src/main.rs" caption="Specifying which trait’s `fly` method we want to call">
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-19/src/main.rs:here}}
</Listing>
વર્ગનામના ઉલ્લેખને પદ્ધતિના નામ પહેલાં સ્પષ્ટ કરવાથી Rust ને ખબર પડે છે કે કયું `fly` અમલીકરણ બોલાવું છે. આપણે `Human::fly(&person)` પણ લખી શકીએ, જે Listing 20-19 માં વપરાયેલ `person.fly()` સમાન છે, પરંતુ જો આપણને ભેદ પાડવાની જરૂર ન હોય તો તે થોડું

લાંબુ લાગે છે. આ કોડ ચલાવવાથી નીચે મુજબ છાપવામાં આવે છે:

{{#include ../listings/ch20-advanced-features/listing-20-19/output.txt}}
કારણ કે `fly` પદ્ધતિ `self` પરિમાણ લે છે, જો આપણી પાસે બે પ્રકારો હોત જે એક trait અમલમાં મૂકે છે, તો Rust એ trait નું કયું અમલીકરણ વાપરવું તે `self` ના પ્રકારના આધારે નક્કી કરી શકતું હતું.

જો કે, સંલગ્ન કાર્યો (functions) જે પદ્ધતિઓ નથી, તેઓ `self` પરિમાણ લેતા નથી. જ્યારે બહુવિધ પ્રકારો અથવા traits હોય છે જે સમાન કાર્ય નામ સાથે non-method કાર્યો વ્યાખ્યાયિત કરે છે, ત્યારે Rust ને હંમેશા ખબર હોતી નથી કે તમે કયા પ્રકારનો ઉલ્લેખ કરી રહ્યા છો સિવાય કે તમે સંપૂર્ણ રીતે લાયક વાક્યરચના (syntax) નો ઉપયોગ કરો. દાખલા તરીકે, યાદી 20-20 માં, અમે એક પ્રાણી આશ્રય માટે trait બનાવીએ છીએ જે તમામ બચ્ચાં કૂતરાંને Spot નામ આપવા માંગે છે. અમે `Animal` trait સાથે એક સંલગ્ન non-method કાર્ય `baby_name` બનાવીએ છીએ. `Animal` trait ને struct `Dog` માટે અમલમાં મૂકવામાં આવે છે, જેના પર અમે સીધું જ એક સંલગ્ન non-method કાર્ય `baby_name` પણ પ્રદાન કરીએ છીએ.

<Listing number="20-20" file-name="src/main.rs" caption="A trait with an associated function and a type with an associated function of the same name that also implements the trait">
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-20/src/main.rs}}
</Listing>
અમે `Dog` પ્રકાર પર વ્યાખ્યાયિત થયેલ `baby_name` સાંકળ કાર્યમાં બધા કૂતરાઓને સ્પૉટ નામ આપવા માટે કોડનો અમલ કરીએ છીએ. `Dog` પ્રકાર પણ `Animal` લક્ષણનો અમલ કરે છે, જે તમામ પ્રાણીઓમાં રહેલા લક્ષણોનું વર્ણન કરે છે. નાના કૂતરાઓને બચ્ચા કહેવામાં આવે છે, અને તે `Animal` લક્ષણના `Dog` પરના અમલીકરણમાં વ્યક્ત થાય છે `baby_name` કાર્ય સાથે સંકળાયેલ છે.

`main` માં, અમે `Dog::baby_name` કાર્યને બોલાવીએ છીએ, જે સીધું જ `Dog` પર વ્યાખ્યાયિત થયેલ સાંકળ કાર્યને બોલાવે છે. આ કોડ નીચે મુજબ છાપે છે:

{{#include ../listings/ch20-advanced-features/listing-20-20/output.txt}}
આ પરિણામ આપણને જોઈતું નથી. આપણે `Animal` ટ્રેઇટ પર અમલમાં મુકાયેલ `Dog` સાથે `baby_name` ફંક્શનને બોલાવવા માંગીએ છીએ, જેથી કોડ `A baby dog is called a puppy` પ્રિન્ટ કરે. લિસ્ટિંગ 20-19 માં આપણે જે ટ્રેઇટ નામ સ્પષ્ટ કરવાની પદ્ધતિનો ઉપયોગ કર્યો તે અહીં મદદરૂપ થતો નથી; જો આપણે `main` ને લિસ્ટિંગ 20-21 ના કોડમાં બદલીએ, તો આપણને કમ્પાઇલેશન એરર મળશે.

<Listing number="20-21" file-name="src/main.rs" caption="Attempting to call the `baby_name` function from the `Animal` trait, but Rust doesn’t know which implementation to use">
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-21/src/main.rs:here}}
</Listing>
કારણ કે `Animal::baby_name` માં `self` પરિમાણ નથી, અને અન્ય પ્રકારો પણ હોઈ શકે છે જે `Animal` લક્ષણને અમલમાં મૂકે છે, Rust નક્કી કરી શકતું નથી કે આપણે કયા `Animal::baby_name` અમલીકરણ જોઈએ છીએ. આપણને આ compiler ભૂલ મળશે:

{{#include ../listings/ch20-advanced-features/listing-20-21/output.txt}}
અસ્પષ્ટતા દૂર કરવા અને Rustને જણાવવા માટે કે આપણે `Dog` માટે `Animal` નું અમલીકરણ વાપરવા માંગીએ છીએ, અન્ય કોઈ type માટે નહીં, તો આપણે સંપૂર્ણ રીતે લખાણનો ઉપયોગ કરવો જરૂરી છે. સૂચિ 20-22 દર્શાવે છે કે સંપૂર્ણ રીતે લખાણનો કેવી રીતે ઉપયોગ કરવો.

<Listing number="20-22" file-name="src/main.rs" caption="Using fully qualified syntax to specify that we want to call the `baby_name` function from the `Animal` trait as implemented on `Dog`">
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-22/src/main.rs:here}}
</Listing>
અમે Rust ને ખૂણાના કૌંસમાં એક પ્રકારનું નિદર્શન આપી રહ્યા છીએ, જે દર્શાવે છે કે અમે `Animal` ટ્રેઇટ પરથી `baby_name` પદ્ધતિને `Dog` દ્વારા અમલમાં મૂકવા માંગીએ છીએ, એવું કહીને કે અમે આ કાર્ય માટે `Dog` પ્રકારને `Animal` તરીકે ગણવા માંગીએ છીએ. આ કોડ હવે આપણને જે જોઈએ છે તે છાપશે:

{{#include ../listings/ch20-advanced-features/listing-20-22/output.txt}}
સામાન્ય રીતે, સંપૂર્ણ નિશ્ચિત સિન્ટેક્સ આ પ્રમાણે વ્યાખ્યાયિત કરવામાં આવે છે:

<Type as Trait>::function(receiver_if_method, next_arg, ...);
સંબંધિત કાર્યો માટે જે પદ્ધતિઓ નથી, ત્યાં કોઈ `receiver` હોતું નથી: ત્યાં માત્ર અન્ય Argumentોની યાદી જ હોય છે. તમે સંપૂર્ણ રીતે લંબિત વાક્યરચનાનો ઉપયોગ દરેક જગ્યાએ કરી શકો છો જ્યાં તમે કાર્યો અથવા પદ્ધતિઓને બોલાવો છો. જો કે, તમને આ વાક્યરચનાના કોઈપણ ભાગને બાકાત રાખવાની મંજૂરી છે જે Rust પ્રોગ્રામમાં અન્ય માહિતીમાંથી જાણી શકે છે. તમારે માત્ર આ વધુ વિસ્તૃત વાક્યરચનાનો ઉપયોગ એવા કિસ્સાઓમાં કરવાની જરૂર છે જ્યાં બહુવિધ અમલીકરણો હોય છે જે સમાન નામનો ઉપયોગ કરે છે અને Rust ને ઓળખવામાં મદદની જરૂર પડે છે કે તમે કયું અમલીકરણ બોલાવવા માંગો છો.

<!-- Old headings. Do not remove or links may break. -->
### Using Supertraits

ક્યારેક તમે એવા ટ્રેઇટ વ્યાખ્યા (trait definition) લખી શકો છો જે બીજા ટ્રેઇટ પર આધારિત હોય: પ્રથમ ટ્રેઇટને અમલમાં મૂકવા માટે, તમારે ઇચ્છવું જોઈએ કે તે પ્રકાર બીજો ટ્રેઇટ પણ અમલમાં મૂકે. તમે આ એટલા માટે કરશો જેથી તમારી ટ્રેઇટ વ્યાખ્યા બીજા ટ્રેઇટના સંલગ્ન વસ્તુઓનો ઉપયોગ કરી શકે. જે ટ્રેઇટ પર તમારી ટ્રેઇટ વ્યાખ્યા આધારિત છે તેને તમારા ટ્રેઇટનું સુપરટ્રેઇટ કહેવામાં આવે છે.

ઉદાહરણ તરીકે, ચાલો કહીએ કે આપણે એક `OutlinePrint` ટ્રેઇટ બનાવવા માંગીએ છીએ જેમાં `outline_print` નામની પદ્ધતિ (method) હશે જે આપેલ મૂલ્યને ફોર્મેટ કરીને છાપશે જેથી તે તારાઓથી ઘેરાયેલું હોય. એટલે કે, જો આપણી પાસે `Point` સ્ટ્રક્ચુર હોય જે `Display` પ્રમાણભૂત લાઈબ્રેરી ટ્રેઇટને અમલમાં મૂકે છે અને પરિણામ `(x, y)` આવે છે, તો જ્યારે આપણે `outline_print` ને `Point` ઇન્સ્ટન્સ પર કૉલ કરીએ છીએ જેમાં `x` માટે `1` અને `y` માટે `3` હોય, તો તેણે નીચે મુજબ છાપવું જોઈએ:

**********
*        *
* (1, 3) *
*        *
**********
`outline_print` પદ્ધતિના અમલીકરણમાં, આપણે `Display` લક્ષણની કાર્યક્ષમતાનો ઉપયોગ કરવા માંગીએ છીએ. તેથી, આપણે સ્પષ્ટ કરવું પડશે કે `OutlinePrint` લક્ષણ માત્ર એવા પ્રકારો માટે જ કામ કરશે જે `Display` પણ લાગુ કરે છે અને `OutlinePrint` ને જરૂરી કાર્યક્ષમતા પૂરી પાડે છે. આપણે લક્ષણ વ્યાખ્યામાં `OutlinePrint: Display` સ્પષ્ટ કરીને આ કરી શકીએ છીએ. આ તકનીક લક્ષણમાં લક્ષણ બંધ ઉમેરવા જેવું જ છે. સૂચિ 20-23 માં `OutlinePrint` લક્ષણનું એક અમલીકરણ દર્શાવવામાં આવ્યું છે.

<Listing number="20-23" file-name="src/main.rs" caption="Implementing the `OutlinePrint` trait that requires the functionality from `Display`">
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-23/src/main.rs:here}}
</Listing>
`&Self` આપણે ઉલ્લેખ કર્યો છે કે `OutlinePrint` ને `Display` લક્ષણની આવશ્યકતા છે, તેથી આપણે `to_string` કાર્યનો ઉપયોગ કરી શકીએ છીએ જે કોઈપણ પ્રકાર માટે આપમેળે અમલમાં મુકાય છે જે `Display` લાગુ કરે છે. જો આપણે કોલન ઉમેર્યા વિના અને લક્ષણના નામ પછી `Display` લક્ષણને સ્પષ્ટ કર્યા વિના `to_string` નો ઉપયોગ કરવાનો પ્રયાસ કરીએ, તો

આપણને એક ભૂલ મળશે જેમાં જણાવવામાં આવ્યું હશે કે વર્તમાન અવકાશમાં `&Self` પ્રકાર માટે `to_string` નામનું કોઈ કાર્ય મળ્યું નથી. Let’s see what happens when we try to implement `OutlinePrint` on a type that doesn’t implement `Display`, such as the `Point` struct:

<Listing file-name="src/main.rs">
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/src/main.rs:here}}
</Listing>
આપણે એક ભૂલ સંદેશાપામે છીએ કે `Display` જરૂરી છે પણ અમલમાં નથી મૂકાયું:

{{#include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/output.txt}}
આ સમસ્યા નિવારવા માટે, અમે `Point` પર `Display` અમલમાં મૂકીશું અને `OutlinePrint` ને જરૂરી શરત સંતોષીશું, આ પ્રમાણે:

<Listing file-name="src/main.rs">
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-03-impl-display-for-point/src/main.rs:here}}
</Listing>
પછી, `OutlinePrint` ટ્રેઇટને `Point` પર અમલમાં મૂકવાથી તે સફળતાપૂર્વક કમ્પાઇલ થશે, અને અમે `outline_print` ને `Point` ઇન્સ્ટન્સ પર બોલાવી શકીશું જેથી તેને તારાની રૂપરેખામાં દર્શાવી શકાય.

<!-- Old headings. Do not remove or links may break. -->
### Implementing External Traits with the Newtype Pattern

અગાઉના પ્રકરણ ૧૦ માં “એક પ્રકાર પર લક્ષણ અમલમાં મૂકવું” વિભાગમાં, અમે અনাথ નિયમનો ઉલ્લેખ કર્યો હતો કે જેમાં જણાવવામાં આવ્યું છે કે આપણને માત્ર ત્યારે જ કોઈ લક્ષણને એક પ્રકાર પર અમલમાં મૂકવાની મંજૂરી છે જો લક્ષણ અથવા પ્રકાર, અથવા બંને, અમારી ક્રેટ સ્થાનિક હોય. ન્યૂટાઇપ પેટર્નનો ઉપયોગ કરીને આ નિયંત્રણને ટાળવું શક્ય છે, જેમાં એક ટ્યુપલ સ્ટ્રક્ચર બનાવવાનો સમાવેશ થાય છે. (અમે પ્રકરણ ૫ માં “ટ્યુપલ સ્ટ્રક્ચર્સ સાથે વિવિધ પ્રકારો બનાવવું” વિભાગમાં ટ્યુપલ સ્ટ્રક્ચર્સ વિશે વાત કરી હતી.) ટ્યુપલ સ્ટ્રક્ચરમાં એક ક્ષેત્ર હશે અને જે પ્રકાર માટે અમે લક્ષણ અમલમાં મૂકવા માંગીએ છીએ તેના માટે પાતળું આવરણ તરીકે કામ કરશે. પછી, આવરણ પ્રકાર અમારી ક્રેટ સ્થાનિક હોય છે, અને અમે આવરણ પર લક્ષણ અમલમાં મૂકી શકીએ છીએ. ન્યૂટાઇપ એ એક શબ્દ છે જે હેસ્કેલ પ્રોગ્રામિંગ ભાષામાંથી ઉદ્ભવ્યો છે. આ પેટર્નનો ઉપયોગ કરવાથી કોઈ રનટાઈમ પ્રદર્શન દંડ નથી, અને કમ્પાઇલ સમયે આવરણ પ્રકાર દૂર થઈ જાય છે.

એક ઉદાહરણ તરીકે, ચાલો આપણે `Vec<T>` પર `Display` અમલમાં મૂકવા માંગીએ છીએ, જે અનાથ નિયમ (orphan rule) આપણને સીધું કરવાની મંજૂરી આપતો નથી, કારણ કે `Display` ટ્રેઇટ અને `Vec<T>` પ્રકાર અમારી ક્રેટની બહાર વ્યાખ્યાયિત થયેલ છે. આપણે એક `Wrapper` સ્ટ્રક્ચર બનાવી શકીએ છીએ જે `Vec<T>` ની ઇન્સ્ટન્સ ધરાવે છે; પછી, આપણે `Wrapper` પર `Display` અમલમાં મૂકી શકીએ છીએ અને `Vec<T>` મૂલ્યનો ઉપયોગ કરી શકીએ છીએ, જેમ કે લિસ્ટિંગ 20-24 માં દર્શાવેલ છે.

<Listing number="20-24" file-name="src/main.rs" caption="Creating a `Wrapper` type around `Vec<String>` to implement `Display`">
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-24/src/main.rs}}
</Listing>
`Display` ની અમલીકરણ પદ્ધતિ `self.0` નો ઉપયોગ કરે છે જેથી અંદરના `Vec<T>` ને સુલભ બનાવી શકાય, કારણ કે `Wrapper` એક ટ્યૂપ struct છે અને `Vec<T>` એ ટ્યૂપમાં ઇન્ડેક્સ 0 પર રહેલો ઘટક છે. ત્યારબાદ, આપણે `Wrapper` પર `Display`

trait ની કાર્યક્ષમતાનો ઉપયોગ કરી શકીએ છીએ. આ પદ્ધતિનો ગેરલાભ એ છે કે `Wrapper` એક નવો પ્રકાર છે, તેથી તે જે મૂલ્ય ધરાવે છે તેની પદ્ધતિઓ ધરાવતો નથી. આપણે `Wrapper` પર `Vec<T>` ની બધી પદ્ધતિઓ સીધી રીતે અમલમાં મૂકવી પડે, જેથી તે પદ્ધતિઓ `self.0` ને સોંપે, જેનાથી આપણને `Wrapper` ને બરાબર `Vec<T>` જેવું જ ગણી શકાય. જો આપણે ઈચ્છીએ કે નવા પ્રકારમાં અંદરના પ્રકારની દરેક પદ્ધતિ હોય, તો `Wrapper` પર `Deref` trait નો અમલ કરવો એ એક ઉકેલ હોઈ શકે (આપણે પ્રકરણ 15 માં “સ્માર્ટ પોઇન્ટર્સને નિયમિત રેફરન્સ જેમ ગણવા” વિભાગમાં `Deref` trait નો અમલ વિશે ચર્ચા કરી હતી). જો આપણે `Wrapper` પ્રકારને અંદરના પ્રકારની બધી પદ્ધતિઓ ધરાવતો ન હોય એવું ઈચ્છીએ—ઉદાહરણ તરીકે, `Wrapper` પ્રકારનું વર્તન મર્યાદિત કરવા માટે—તો આપણે માત્ર જોઈતી પદ્ધતિઓને જાતે જ અમલમાં મૂકવી પડે.

આ નવું પ્રકારની પેટર્ન અન્ય સ્થિતિઓમાં પણ ઉપયોગી છે, જ્યાં લક્ષણો (traits) સામેલ ન હોય. ચાલો ધ્યાન બદલીએ અને Rust ના પ્રકાર સિસ્ટમ સાથે ક્રિયાપ્રતિક્રિયા કરવાની કેટલીક અદ્યતન રીતો જોઈએ.

