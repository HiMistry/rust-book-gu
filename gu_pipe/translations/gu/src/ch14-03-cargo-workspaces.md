## Cargo Workspaces

પ્રકરણ ૧૨ માં, આપણે એક પેકેજ બનાવ્યું હતું જેમાં બાઈનરી `crate` અને લાઈબ્રેરી `crate` બંનેનો સમાવેશ થતો હતો. જેમ જેમ તમારી યોજના આગળ વધે છે, તેમ તેમ તમને લાગી શકે છે કે લાઈબ્રેરી `crate` વધુ મોટી થતી જાય છે અને તમે તમારા પેકેજને વધુ ભાગોમાં વિભાજીત કરવા માંગો છો. Cargo એક એવી સુવિધા આપે છે જેને વર્કસ્પેસ કહેવાય છે, જે એકસાથે વિકસાવવામાં આવતા બહુવિધ સંબંધિત પેકેજોનું સંચાલન કરવામાં મદદ કરી શકે છે.

### Creating a Workspace

કાર્યસ્થળ એ પેકેજોનો સમૂહ છે જે સમાન `Cargo.lock` અને આઉટપુટ ડિરેક્ટરી વહેંચે છે. ચાલો આપણે કાર્યસ્થળનો ઉપયોગ કરીને એક પ્રોજેક્ટ બનાવીએ—આપણે સરળ કોડનો ઉપયોગ કરીશું જેથી આપણે કાર્યસ્થળની રચના પર ધ્યાન કેન્દ્રિત કરી શકીએ. કાર્યસ્થળને રચવાના ઘણાં વિવિધ માર્ગો છે, તેથી આપણે માત્ર એક સામાન્ય રીત બતાવીશું. આપણી પાસે એક બાઈનરી અને બે લાયબ્રેરીઓ ધરાવતું કાર્યસ્થળ હશે. બાઈનરી, જે મુખ્ય કાર્યક્ષમતા પ્રદાન કરશે, તે બે લાયબ્રેરીઓ પર આધારિત રહેશે. એક લાયબ્રેરી `add_one` ફંક્શન પ્રદાન કરશે અને બીજી લાયબ્રેરી `add_two` ફંક્શન પ્રદાન કરશે. આ ત્રણ `crate` સમાન કાર્યસ્થળનો ભાગ હશે. આપણે નવા ડિરેક્ટરી બનાવીને શરૂઆત કરીશું:

$ mkdir add
$ cd add
આગળ, `add` ડિરેક્ટરીમાં, આપણે `Cargo.toml` ફાઈલ બનાવીશું જે સમગ્ર વર્કસ્પેસને રૂપરેખાંકિત કરશે. આ ફાઈલમાં `[package]` વિભાગ નહીં હોય. તેના બદલે, તેમાં `[workspace]` વિભાગ હશે જે આપણને વર્કસ્પેસમાં સભ્યો ઉમેરવાની મંજૂરી આપશે. આપણે એ પણ ધ્યાન રાખીએ છીએ કે વર્કસ્પેસમાં Cargoના નવીનતમ રિઝોલ્વર અલ્ગોરિધમનો ઉપયોગ કરીએ, `resolver` મૂલ્યને `"3"` પર સેટ કરીને:

ફાઈલનું નામ: Cargo.toml

{{#include ../listings/ch14-more-about-cargo/no-listing-01-workspace/add/Cargo.toml}}
આગળ, આપણે `adder` બાઈનરી ક્રેટ બનાવશું, જે `cargo new` આદેશ ચલાવીને `add` ડિરેક્ટરીમાં કરશે:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-01-adder-crate/add
remove `members = ["adder"]` from Cargo.toml
rm -rf adder
cargo new adder
copy output below
-->
$ cargo new adder
     Created binary (application) `adder` package
      Adding `adder` as member of workspace at `file:///projects/add`
કાર્યકારી `cargo new` વર્કિંગ એરિયામાં પણ આપોઆપ નવું પેકેજ `members` કીમાં ઉમેરાય છે, જે `[workspace]` વ્યાખ્યામાં વર્કિંગ એરિયા Cargo.toml માં જોવા મળે છે, આ પ્રમાણે:

{{#include ../listings/ch14-more-about-cargo/output-only-01-adder-crate/add/Cargo.toml}}
હવે, આપણી કાર્યક્ષેત્ર બનાવી શકીએ છીએ `cargo build` ચલાવીને. તમારા ‘add’ ડિરેક્ટરીમાં રહેલી ફાઈલો આ પ્રમાણે દેખાવા જોઈએ:

├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
કાર્યસ્થળમાં એક લક્ષ્ય ડિરેક્ટરી ટોચના સ્તર પર હોય છે જેમાં કમ્પાઈલ કરેલા આર્ટિફેક્ટ્સ મૂકવામાં આવે છે; `adder` પેકેજની પોતાની લક્ષ્ય ડિરેક્ટરી નથી. ભલે આપણે `adder` ડિરેક્ટરીની અંદરથી `cargo build` ચલાવીએ, તો પણ કમ્પાઈલ કરેલા આર્ટિફેક્ટ્સ add/target માં જ આવશે, add/adder/target માં નહીં. કાર્ગો કાર્યસ્થળમાં લક્ષ્ય ડિરેક્ટરીને આ રીતે ગોઠવે છે કારણ કે વર્કસ્પેસમાં રહેલા ક્રેટ્સ એકબીજા પર આધાર રાખવા માટે બનાવાયેલા હોય છે. જો દરેક ક્રેટની પોતાની લક્ષ્ય ડિરેક્ટરી હોત, તો દરેક ક્રેટને વર્કસ્પેસમાંના અન્ય તમામ ક્રેટ્સને ફરીથી કમ્પાઈલ કરવા પડ્યા હોત જેથી આર્ટિફેક્ટ્સ તેની પોતાની લક્ષ્ય ડિરેક્ટરીમાં મૂકી શકાય. એક જ લક્ષ્ય ડિરેક્ટરી વહેંચીને, ક્રેટ્સ બિનજરૂરી પુનઃનિર્માણ ટાળી શકે છે.

### Creating the Second Package in the Workspace

હવે, કાર્યસ્થળમાં બીજા સભ્ય પેકેજનું નિર્માણ કરીએ અને તેને `add_one` નામ આપીએ. `add_one` નામની નવી લાયબ્રેરી ક્રેટ બનાવો:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-02-add-one/add
remove `"add_one"` from `members` list in Cargo.toml
rm -rf add_one
cargo new add_one --lib
copy output below
-->
$ cargo new add_one --lib
     Created library `add_one` package
      Adding `add_one` as member of workspace at `file:///projects/add`
ફાઈલનામ: Cargo.toml ઉચ્ચ સ્તરનું Cargo.toml હવે `members` યાદીમાં add_one માર્ગનો

સમાવેશ કરશે:

{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/Cargo.toml}}
તમારું ઉમેરાયેલું ડિરેક્ટરીમાં હવે આ ડિરેક્ટરીઓ અને ફાઈલો હોવી જોઈએ:

├── Cargo.lock
├── Cargo.toml
├── add_one
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
ફાઈલ `add_one/src/lib.rs` માં, ચાલો એક `add_one` વિધેય

ઉમેરીએ: Filename: add_one/src/lib.rs

{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/add_one/src/lib.rs}}
હવે આપણે `adder` પેકેજને આપણી બાઈનરી પર આધાર રાખે તેવું કરી શકીએ છીએ, જે `add_one` પેકેજ પર આધારિત છે જેમાં આપણો લાયબ્રેરી છે. પ્રથમ, આપણે `adder/Cargo.toml` માં `add_one` પર એક પાથ ડિપેન્ડન્સી ઉમેરવાની જરૂર પડશે.

ફાઈલનામ: adder/Cargo.toml

{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/adder/Cargo.toml:6:7}}
Cargo કોઈ ધારી લેતું નથી કે વર્કસ્પેસમાં રહેલા crates એકબીજા પર આધારિત છે, તેથી આપણે અવલંબન સંબંધો વિશે સ્પષ્ટપણે જણાવવાની જરૂર છે.

આગળ, ચાલો `add_one` ફંક્શન ( `add_one` crate માંથી) ને `adder` crate માં વાપરીએ. `adder/src/main.rs` ફાઈલ ખોલો અને `main` ફંક્શનને Listing 14-7 ની જેમ `add_one` ફંક્શનને બોલાવવા માટે બદલો.

<Listing number="14-7" file-name="adder/src/main.rs" caption="Using the `add_one` library crate from the `adder` crate">
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-07/add/adder/src/main.rs}}
</Listing>
ચાલો વર્કસ્પેસ બનાવીએ `cargo build` આદેશ ચલાવીને ટોપ-લેવલ ઉમેરવાની ડિરેક્ટરીમાં!

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->
$ cargo build
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
આ બાઈનરી `crate` ને `add` ડિરેક્ટરીમાંથી ચલાવવા માટે, આપણે `-p` આર્ગ્યુમેન્ટ અને પેકેજ નામના ઉપયોગથી વર્કસ્પેસમાં કયું પેકેજ ચલાવવું છે તે સ્પષ્ટ કરી શકીએ છીએ: `cargo run`.

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo run -p adder
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->
$ cargo run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/adder`
Hello, world! 10 plus one is 11!
આ કોડ adder/src/main.rs માં ચલાવવામાં આવે છે, જે `add_one` ક્રેટ પર આધારિત છે.

<!-- Old headings. Do not remove or links may break. -->
### Depending on an External Package

ધ્યાન કરો કે વર્કસ્પેસમાં માત્ર એક જ Cargo.lock ફાઈલ ટોપ લેવલ પર છે, દરેક ક્રેટની ડિરેક્ટરીમાં નહીં. આ સુનિશ્ચિત કરે છે કે બધા ક્રેટ્સ તમામ નિર્ભરતાઓના સમાન સંસ્કરણનો ઉપયોગ કરી રહ્યા છે. જો આપણે `rand` પેકેજને adder/Cargo.toml અને add_one/Cargo.toml ફાઇલોમાં ઉમેરીએ, તો Cargo તે બંનેને `rand` ના એક સંસ્કરણમાં ઉકેલશે અને તેને એક જ Cargo.lock માં નોંધશે. વર્કસ્પેસના બધા ક્રેટ્સ સમાન નિર્ભરતાનો ઉપયોગ કરે છે એનો અર્થ થાય છે કે ક્રેટ્સ હંમેશા એકબીજા સાથે સુસંગત રહેશે. ચાલો `rand` ક્રેટને add_one/Cargo.toml ફાઇલના `[dependencies]` વિભાગમાં ઉમેરીએ જેથી આપણે `add_one` ક્રેટમાં `rand` ક્રેટનો ઉપયોગ કરી શકીએ:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:
* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
-->
add_one/Cargo.toml આ `Cargo.toml` ફાઈલ એક `crate` માટે રૂપરેખાંકન માહિતી ધરાવે છે. આ રૂપરેખાંકનમાં `crate`નું નામ, સંસ્કરણ, લેખક અને અન્ય સંબંધિત વિગતો સમાવિષ્ટ છે જે `rustup` અને `cargo` જેવા સાધનો દ્વારા ઉપયોગમાં લેવાય છે. આ ફાઈલ `project`ના મૂળ ડિરેક્ટરીમાં સ્થિત હોવી જોઈએ. [package] name = "add_one" version = "0.1.0" authors = ["Your Name <your_email@example.com>"] edition = "2021" [dependencies]

{{#include ../listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add/add_one/Cargo.toml:6:7}}
હવે આપણે `use rand;` ને add_one/src/lib.rs ફાઈલમાં ઉમેરી શકીએ છીએ, અને `cargo build` આદેશ ચલાવીને સમગ્ર વર્કસ્પેસ બનાવવાથી `rand` ક્રેટે આયાત થશે અને સંકલિત થશે. આપણને એક ચેતવણી મળશે કારણ કે આપણે જે `rand` ને અવકાશમાં લાવ્યા છીએ તેનો ઉલ્લેખ નથી કરી રહ્યા:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->
$ cargo build
    Updating crates.io index
  Downloaded rand v0.8.5
   --snip--
   Compiling rand v0.8.5
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
warning: unused import: `rand`
 --> add_one/src/lib.rs:1:5
  |
1 | use rand;
  |     ^^^^
  |
  = note: `#[warn(unused_imports)]` on by default

warning: `add_one` (lib) generated 1 warning (run `cargo fix --lib -p add_one` to apply 1 suggestion)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.95s
ટોચનું Cargo.lock હવે `add_one` નું `rand` પર નિર્ભરતા વિશે માહિતી ધરાવે છે. જોકે, ભલે `rand` વર્કસ્પેસમાં ક્યાંક વપરાયેલું હોય, તે વર્કસ્પેસમાં અન્ય ક્રેટ્સમાં ઉપયોગ કરી શકાતું નથી સિવાય કે આપણે તેમના Cargo.toml ફાઇલોમાં પણ `rand` ઉમેર્યું હોય. ઉદાહરણ તરીકે, જો આપણે `use rand;` ને adder/src/main.rs ફાઈલમાં `adder` પેકેજ માટે ઉમેરીએ, તો આપણને ભૂલ મળશે:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-03-use-rand/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->
$ cargo build
  --snip--
   Compiling adder v0.1.0 (file:///projects/add/adder)
error[E0432]: unresolved import `rand`
 --> adder/src/main.rs:2:5
  |
2 | use rand;
  |     ^^^^ no external crate `rand`
આ સુધારવા માટે, `adder` પેકેજ માટેની Cargo.toml ફાઈલ સંપાદિત કરો અને દર્શાવો કે `rand` તેની નિર્ભરતા (dependency) છે. `adder` પેકેજ બનાવવાથી `rand` ને `adder` માં નિર્ભરતાઓની યાદીમાં ઉમેરાશે Cargo.lock માં, પરંતુ `rand` ની કોઈ વધારાની નકલો ડાઉનલોડ થશે નહીં. Rust ખાતરી કરશે કે વર્કિંગ સ્પેસ (workspace) માં દરેક પેકેજમાં દરેક crate `rand` પેકેજનો સમાન સંસ્કરણ વાપરે છે જ્યાં સુધી તેઓ `rand` ના સુસંગત સંસ્કરણોનો ઉલ્લેખ કરે, જેનાથી આપણી જગ્યા બચે અને વર્કિંગ સ્પેસમાંના crates એકબીજા સાથે સુસંગત રહે.

જો વર્કસ્પેસમાં રહેલા ક્રેટે એક જ આધારિત પેકેજ (dependency) ના અસંગત સંસ્કરણોનો ઉલ્લેખ કરે છે, તો Cargo દરેકને ઉકેલવાનો પ્રયત્ન કરશે પરંતુ શક્ય હોય ત્યાં સુધી ઓછા સંસ્કરણોનો ઉપયોગ કરવાનો પ્રયાસ કરશે.

### Adding a Test to a Workspace

વધુ એક સુધારણા માટે, ચાલો `add_one::add_one` વિધેયનું પરીક્ષણ `add_one` ક્રેટમાં ઉમેરીએ:

ફાઈલનામ: add_one/src/lib.rs

{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add/add_one/src/lib.rs}}
હવે ટોચના સ્તરના ઉમેરણ ડિરેક્ટરીમાં `cargo test` ચલાવો. આ પ્રકારની રચના ધરાવતા વર્કસ્પેસમાં `cargo test` ચલાવવાથી વર્કસ્પેસમાં રહેલા તમામ ક્રેટે માટે પરીક્ષણો થશે:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test
copy output below; the output updating script doesn't handle subdirectories in
paths properly
-->
$ cargo test
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/adder-3a47283c568d2b6a)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
પહેલો ભાગ પ્રથમ વિભાગ દર્શાવે છે કે `it_works` પરીક્ષણ `add_one` ક્રેટમાં સફળ થયું. આગળનો વિભાગ દર્શાવે છે કે `adder` ક્રેટમાં શૂન્ય પરીક્ષણો મળ્યા, અને અંતિમ વિભાગ દર્શાવે છે કે `add_one` ક્રેટમાં શૂન્ય દસ્તાવેજીકરણ પરીક્ષણો મળ્યા. અમે વર્કસ્પેસમાં

એક ચોક્કસ ક્રેટ માટે પણ `-p` ધ્વજ વાપરીને અને જે ક્રેટનું પરીક્ષણ આપણે કરવા માંગીએ છીએ તેનું નામ સ્પષ્ટ કરીને ટોચના સ્તરની ડિરેક્ટરીમાંથી પરીક્ષણો ચલાવી શકીએ છીએ:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test -p add_one
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->
$ cargo test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
આ પરિણામ દર્શાવે છે કે `cargo test` આદેશ માત્ર `add_one` ક્રેઇટ માટે પરીક્ષણો ચલાવ્યા અને `adder` ક્રેઇટના પરીક્ષણો ચલાવ્યા ન હતા.

જો તમે વર્કસ્પેસમાં રહેલા ક્રેઇટ્સને crates.io પર પ્રકાશિત કરો છો, તો વર્કસ્પેસમાં દરેક ક્રેઇટને અલગથી પ્રકાશિત કરવાની જરૂર પડશે. `cargo test` ની જેમ, અમે `-p` ધ્વજ વાપરીને અને જે ક્રેઇટ પ્રકાશિત કરવા માંગીએ છીએ તેનું નામ સ્પષ્ટ કરીને અમારા વર્કસ્પેસમાં કોઈ ચોક્કસ ક્રેઇટ પ્રકાશિત કરી શકીએ છીએ.

વધારાના અભ્યાસ માટે, `add_two` ક્રેઇટને `add_one` ક્રેઇટની જેમ જ આ વર્કસ્પેસમાં ઉમેરો!

જેમ જેમ તમારી યોજના વિસ્તરે છે, તેમ તેમ વર્કસ્પેસનો ઉપયોગ કરવાનું વિચારો: તે તમને એક મોટા કોડ સમૂહને બદલે નાના, સમજવામાં સરળ ઘટકો સાથે કામ કરવાની મંજૂરી આપે છે. વધુમાં, વર્કસ્પેસમાં ક્રેટેસ રાખવાથી જો તેઓ એકસાથે વારંવાર બદલાતા હોય તો તેમની વચ્ચે સંકલન સરળ બની શકે છે.

