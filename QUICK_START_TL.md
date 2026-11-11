# Mabilisang Gabay sa GATUZ

Simple guide para makapagsimula sa GATUZ Egg Farm Management System.

## Unang beses gamitin

1. I-install ang **Python 3.12 o mas bago** sa Windows.
2. I-download o i-clone ang repository, at i-extract kung ZIP ang nakuha.
3. I-double-click ang `START_GATUZ.bat` sa root folder. Kailangan ng internet sa unang run para ma-install ang Python packages.
4. Mag-sign in gamit ang initial account kung hindi pa ito napapalitan: `admin` / `admin123`.
5. **Palitan agad ang default password bago maglagay ng totoong farm data.** Sa kasalukuyang UI, maaaring mag-reset ng password ang admin sa **Users**. Hindi pa nakikita sa navigation ang sariling password-change option para sa staff users.

> Kung ayaw magbukas, tiyaking naka-install ang Python at subukang patakbuhin muli ang `START_GATUZ.bat`. Huwag burahin ang `data` o `backups` folder para lang ayusin ang startup.

## Saan pupunta sa app?

- **Dashboard** — mabilisang buod ng itlog, sales, bayad, balance, at gastos.
- **Farms** — magdagdag o mag-edit ng farm. Piliin ang farm sa filter para farm-specific ang mga susunod na entry.
- **Chicken Records** — magtala ng flock o batch.
- **Egg Production** — ilagay ang daily egg counts ayon sa grade.
- **Inventory** — tingnan ang stock at mag-record ng stock in/out.
- **Customers** at **Sales** — magtala ng customer at benta.
- **Expenses** — magtala ng gastusin.
- **Reports** — mag-export ng Excel o PDF summary.
- **Backup & restore** — gumawa ng backup o ibalik ang database mula sa backup file.
- **Users** — admin lang ang may access para sa user management at password reset.

### Bago magdagdag ng records

- Gumawa o piliin muna ang tamang farm sa **Farm view** filter.
- Suriin ang petsa, dami, at presyo bago pindutin ang **Save**.
- Ang delete ay maaaring permanente; mag-backup muna kung hindi sigurado.

## Ingatan ang records

Gumawa ng backup sa **Backup & restore → Create manual backup** at magtabi ng kopya sa ligtas na lokasyon na hiwalay sa project folder. Ang restore ay papalit sa kasalukuyang database, kaya tiyaking tama ang napiling backup.

Ang repository ay may kasamang tracked na SQLite database/backup files. Dahil dito, maaaring nakikita ng sinumang may access sa repository ang laman ng mga ito. Huwag maglagay ng totoong customer o farm records hangga't hindi nasusuri at napoprotektahan ang repository at database. Ang `.gitignore` ay hindi nag-aalis ng files na na-track na.

## Mahalagang limitasyon

Ang kasalukuyang app ay may flock records, pero hindi hiwalay na mortality/culling log. Hindi rin dapat ipagpalagay na mayroon itong morning/afternoon egg collection, hen-day production, o vaccination module. Bago magdagdag ng mga ito, suriin muna ang existing app para maiwasan ang duplicate features.
