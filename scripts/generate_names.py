#!/usr/bin/env python3
"""One-time helper to regenerate name list files."""
from pathlib import Path

FIRST = (
    "James,Mary,John,Patricia,Robert,Jennifer,Michael,Linda,William,Elizabeth,"
    "David,Barbara,Richard,Susan,Joseph,Jessica,Thomas,Sarah,Charles,Karen,"
    "Christopher,Nancy,Daniel,Lisa,Matthew,Betty,Anthony,Margaret,Mark,Sandra,"
    "Donald,Ashley,Steven,Kimberly,Paul,Emily,Andrew,Donna,Joshua,Michelle,"
    "Kenneth,Dorothy,Kevin,Carol,Brian,Amanda,George,Melissa,Edward,Deborah,"
    "Ronald,Stephanie,Timothy,Rebecca,Jason,Sharon,Jeffrey,Laura,Ryan,Emma,"
    "Jacob,Olivia,Gary,Ava,Nicholas,Isabella,Eric,Sophia,Jonathan,Mia,"
    "Stephen,Abigail,Larry,Ella,Justin,Madison,Scott,Chloe,Brandon,Grace,"
    "Benjamin,Victoria,Samuel,Amelia,Frank,Alexis,Gregory,Harper,Raymond,Camila,"
    "Alexander,Luna,Patrick,Eleanor,Jack,Hannah,Jerry,Lily,Dennis,Aubrey,"
    "Tyler,Addison,Aaron,Brooklyn,Jose,Scarlett,Adam,Natalie,Nathan,Leah,"
    "Zachary,Zoe,Kyle,Samantha,Noah,Aria,Ethan,Audrey,Jeremy,Claire"
).split(",")

LAST = (
    "Smith,Johnson,Williams,Brown,Jones,Garcia,Miller,Davis,Rodriguez,Martinez,"
    "Hernandez,Lopez,Gonzalez,Wilson,Anderson,Thomas,Taylor,Moore,Jackson,Martin,"
    "Lee,Perez,Thompson,White,Harris,Sanchez,Clark,Ramirez,Lewis,Robinson,"
    "Walker,Young,Allen,King,Wright,Scott,Torres,Nguyen,Hill,Flores,"
    "Green,Adams,Nelson,Baker,Hall,Rivera,Campbell,Mitchell,Carter,Roberts,"
    "Gomez,Phillips,Evans,Turner,Diaz,Parker,Cruz,Edwards,Collins,Reyes,"
    "Stewart,Morris,Morales,Murphy,Cook,Rogers,Gutierrez,Ortiz,Morgan,Cooper,"
    "Peterson,Bailey,Reed,Kelly,Howard,Ramos,Kim,Cox,Ward,Richardson,"
    "Watson,Brooks,Chavez,Wood,James,Bennett,Gray,Mendoza,Ruiz,Hughes,"
    "Price,Alvarez,Castillo,Sanders,Patel,Myers,Long,Ross,Foster,Jimenez,"
    "Powell,Jenkins,Perry,Russell,Sullivan,Bell,Coleman,Butler,Henderson,Barnes,"
    "Gonzales,Fisher,Vasquez,Simmons,Romero,Jordan,Patterson,Alexander,Hamilton,Graham,"
    "Reynolds,Griffin,Wallace,Moreno,West,Cole,Hayes,Bryant,Herrera,Gibson,"
    "Ellis,Tran,Medina,Aguilar,Stevens,Murray,Ford,Castro,Marshall,Owens,"
    "Harrison,Fernandez,McDonald,Woods,Washington,Kennedy,Wells,Vargas,Henry,Chen"
).split(",")

if __name__ == "__main__":
    base = Path(__file__).parent
    (base / "first_names.txt").write_text("\n".join(FIRST))
    (base / "last_names.txt").write_text("\n".join(LAST))
    print(f"Wrote {len(FIRST)} first names and {len(LAST)} last names")
