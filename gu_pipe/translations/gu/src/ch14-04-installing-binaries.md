<!-- Old headings. Do not remove or links may break. -->
## `cargo install` સાથે બાઈનરી સ્થાપિત કરવું

`cargo install` આદેશ તમને સ્થાનિક રીતે બાઈનરી ક્રેટ સ્થાપિત કરવા અને તેનો ઉપયોગ કરવાની મંજૂરી આપે છે. આ સિસ્ટમ પેકેજોને બદલવા માટે નથી; તે Rust વિકાસકર્તાઓ માટે crates.io પર અન્ય લોકોએ શેર કરેલા સાધનો સ્થાપિત કરવાનો એક અનુકૂળ માર્ગ હોવાનો હેતુ છે. નોંધ કરો કે તમે ફક્ત એવા પેકેજો સ્થાપિત કરી શકો છો જેમાં બાઈનરી લક્ષ્યો હોય. બાઈનરી લક્ષ્ય એ ચાલતી પ્રોગ્રામ છે જે બનાવવામાં આવે છે જો ક્રેટમાં `src/main.rs` ફાઇલ અથવા અન્ય ફાઇલ હોય જે બાઈનરી તરીકે નિર્દિષ્ટ થયેલ હોય, વિપરીત રીતે લાઈબ્રેરી લક્ષ્ય કે જે પોતાની જાતે ચલાવવા યોગ્ય નથી પરંતુ અન્ય પ્રોગ્રામ્સમાં સમાવેશ કરવા માટે યોગ્ય છે. સામાન્ય રીતે, ક્રેટમાં README ફાઇલમાં માહિતી હોય છે કે ક્રેટ લાઇબ્રેરી છે કે નહીં, તેમાં બાઈનરી લક્ષ્ય છે કે નહીં, અથવા બંને.

બધા બાઈનરીઓ જે `cargo install` સાથે સ્થાપિત થાય છે, તે ઇન્સ્ટોલેશન મૂળના bin ફોલ્ડરમાં સંગ્રહિત થાય છે. જો તમે rustup.rs નો ઉપયોગ કરીને Rust સ્થાપિત કર્યું હોય અને તમારી પાસે કોઈ કસ્ટમ રૂપરેખાંકનો ન હોય, તો આ ડિરેક્ટરી $HOME/.cargo/bin હશે. `cargo install` સાથે સ્થાપિત પ્રોગ્રામ્સ ચલાવવા માટે, ખાતરી કરો કે આ ડિરેક્ટરી તમારા `$PATH` માં

છે. ઉદાહરણ તરીકે, પ્રકરણ 12 માં અમે ઉલ્લેખ કર્યો હતો કે ફાઇલો શોધવા માટે `grep` ટૂલનું Rust અમલીકરણ `ripgrep` નામથી ઉપલબ્ધ છે. `ripgrep` સ્થાપિત કરવા માટે, આપણે નીચે મુજબ ચલાવી શકીએ છીએ:

<!-- manual-regeneration
cargo install something you don't have, copy relevant output below
-->
$ cargo install ripgrep
    Updating crates.io index
  Downloaded ripgrep v14.1.1
  Downloaded 1 crate (213.6 KB) in 0.40s
  Installing ripgrep v14.1.1
--snip--
   Compiling grep v0.3.2
    Finished `release` profile [optimized + debuginfo] target(s) in 6.73s
  Installing ~/.cargo/bin/rg
   Installed package `ripgrep v14.1.1` (executable `rg`)
The second-to-last line of the output shows the location and the name of the installed binary, which in the case of `ripgrep` is `rg`. As long as the installation directory is in your `$PATH`, as mentioned previously, you can then run `rg --help` and start using a faster, Rustier tool for searching files! અંતિમ પરંતુ પૂર્વેના છેલ્લા લીટી આઉટપુટમાં સ્થાપિત બાઈનરીનું સ્થાન અને નામ દર્શાવે છે, જે `ripgrep` ના કિસ્સામાં `rg` છે. જ્યાં સુધી સ્થાપન ડિરેક્ટરી તમારા `$PATH` માં હોય, અગાઉ જણાવ્યા મુજબ, તમે પછી `rg --help` ચલાવી શકો છો અને ફાઇલો શોધવા માટે એક ઝડપી, Rustier સાધનનો ઉપયોગ કરવાનું શરૂ કરી શકો છો!

