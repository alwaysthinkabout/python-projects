# -*- coding: utf-8 -*-

import pickle

obj = [{'amounts': 646078.3958072609, 'currency': 'btcusdt', 'counts': 4663378, 'vols': 5050983136.565234}, {'amounts': 1388421.7711351984, 'currency': 'bchusdt', 'counts': 937179, 'vols': 1341529328.920878}, {'amounts': 4837759.389615674, 'currency': 'ethusdt', 'counts': 3099378, 'vols': 2428196907.9908113}, {'amounts': 25824057.22376848, 'currency': 'etcusdt', 'counts': 658283, 'vols': 434318618.4522771}, {'amounts': 5137901.326489421, 'currency': 'ltcusdt', 'counts': 767968, 'vols': 675058833.4147893}, {'amounts': 342598670.55003625, 'currency': 'eosusdt', 'counts': 2754160, 'vols': 3412655587.712059}, {'amounts': 1659179491.0960464, 'currency': 'xrpusdt', 'counts': 901255, 'vols': 1116837557.5142329}, {'amounts': 29286586.237670243, 'currency': 'omgusdt', 'counts': 465394, 'vols': 405630035.86566895}, {'amounts': 1024477.7414220597, 'currency': 'dashusdt', 'counts': 255971, 'vols': 373137325.0727164}, {'amounts': 612449.6017887901, 'currency': 'zecusdt', 'counts': 191784, 'vols': 132594659.90578628}, {'amounts': 322024823.2550801, 'currency': 'adausdt', 'counts': 217010, 'vols': 91110277.11758375}, {'amounts': 14234086.152526615, 'currency': 'ctxcusdt', 'counts': 44798, 'vols': 23633215.529048257}, {'amounts': 75037692.57297724, 'currency': 'actusdt', 'counts': 100732, 'vols': 23131228.41939393}, {'amounts': 251525377.17999414, 'currency': 'btmusdt', 'counts': 1066512, 'vols': 249875577.09999344}, {'amounts': 216377230.76870307, 'currency': 'btsusdt', 'counts': 194340, 'vols': 53210527.22521261}, {'amounts': 38293002.25454363, 'currency': 'ontusdt', 'counts': 454589, 'vols': 172548173.30603963}, {'amounts': 17081474107.421698, 'currency': 'iostusdt', 'counts': 1086622, 'vols': 615905411.9144428}, {'amounts': 630293052.6923115, 'currency': 'htusdt', 'counts': 950104, 'vols': 1137654982.0501256}, {'amounts': 4451445165.807911, 'currency': 'trxusdt', 'counts': 546021, 'vols': 220053020.10799435}, {'amounts': 9678252098.43375, 'currency': 'dtausdt', 'counts': 495164, 'vols': 121710778.5363403}, {'amounts': 1877898.7532247757, 'currency': 'neousdt', 'counts': 560825, 'vols': 115224822.08737734}, {'amounts': 7547922.486064079, 'currency': 'qtumusdt', 'counts': 561250, 'vols': 127143331.9589475}, {'amounts': 3075184.5328560155, 'currency': 'elausdt', 'counts': 627250, 'vols': 114263183.36722647}, {'amounts': 22929228.08941065, 'currency': 'venusdt', 'counts': 449281, 'vols': 69302750.10403961}, {'amounts': 760386245.5448205, 'currency': 'thetausdt', 'counts': 397230, 'vols': 94614800.69155294}, {'amounts': 912003555.5636185, 'currency': 'sntusdt', 'counts': 336037, 'vols': 104197684.50563793}, {'amounts': 2694983287.7855983, 'currency': 'zilusdt', 'counts': 507033, 'vols': 167399112.97169915}, {'amounts': 187348445.79885164, 'currency': 'xemusdt', 'counts': 389706, 'vols': 54644521.96807503}, {'amounts': 12318129.652659848, 'currency': 'nasusdt', 'counts': 446613, 'vols': 67385759.8022141}, {'amounts': 1482406391.7150447, 'currency': 'ruffusdt', 'counts': 437444, 'vols': 104602133.95054175}, {'amounts': 11522746.653879544, 'currency': 'hsrusdt', 'counts': 491144, 'vols': 86271339.60007995}, {'amounts': 1563493133.0922601, 'currency': 'letusdt', 'counts': 288022, 'vols': 68049513.00744657}, {'amounts': 1016191329.4975936, 'currency': 'mdsusdt', 'counts': 565148, 'vols': 91152215.2302951}, {'amounts': 91960902.9853892, 'currency': 'storjusdt', 'counts': 376246, 'vols': 80532714.08808865}, {'amounts': 182852521.7579791, 'currency': 'elfusdt', 'counts': 600463, 'vols': 152789966.23433128}, {'amounts': 78078445.03142932, 'currency': 'itcusdt', 'counts': 441749, 'vols': 87811399.26876782}, {'amounts': 216973836.54411536, 'currency': 'cvcusdt', 'counts': 404290, 'vols': 63161008.70497476}, {'amounts': 292203323.6575577, 'currency': 'gntusdt', 'counts': 387316, 'vols': 114828128.36829224}, {'amounts': 179483.79820000002, 'currency': 'bchbtc', 'counts': 338816, 'vols': 21315.577851135804}, {'amounts': 818172.7496, 'currency': 'ethbtc', 'counts': 3086175, 'vols': 51556.28731185009}, {'amounts': 488088.43630000006, 'currency': 'ltcbtc', 'counts': 198216, 'vols': 8199.4487466012}, {'amounts': 3191526.305400001, 'currency': 'etcbtc', 'counts': 175584, 'vols': 6759.862395802798}, {'amounts': 43587511.015257366, 'currency': 'eosbtc', 'counts': 975983, 'vols': 52231.798899962385}, {'amounts': 6400763.794989986, 'currency': 'omgbtc', 'counts': 249942, 'vols': 10770.910167386555}, {'amounts': 273386862.46346706, 'currency': 'xrpbtc', 'counts': 275667, 'vols': 22934.74270083246}, {'amounts': 293019.6025912798, 'currency': 'dashbtc', 'counts': 150566, 'vols': 13991.035159375984}, {'amounts': 326501.40005854354, 'currency': 'zecbtc', 'counts': 122501, 'vols': 9319.310550317234}, {'amounts': 159451318.18755534, 'currency': 'adabtc', 'counts': 162852, 'vols': 5128.471369177008}, {'amounts': 358014117.4100635, 'currency': 'btmbtc', 'counts': 890408, 'vols': 34790.53514082792}, {'amounts': 82870727.91251099, 'currency': 'ontbtc', 'counts': 591490, 'vols': 36210.55251475199}, {'amounts': 5442075038.863709, 'currency': 'iostbtc', 'counts': 755439, 'vols': 24502.663565814666}, {'amounts': 450117988.5463517, 'currency': 'htbtc', 'counts': 555222, 'vols': 107201.22061953302}, {'amounts': 15558385287.65257, 'currency': 'trxbtc', 'counts': 627951, 'vols': 86715.44718310836}, {'amounts': 6591728.0319915805, 'currency': 'elabtc', 'counts': 663435, 'vols': 30345.882341234243}, {'amounts': 217237380.1126907, 'currency': 'wiccbtc', 'counts': 323041, 'vols': 21739.929824070667}, {'amounts': 30546658999.22788, 'currency': 'ocnbtc', 'counts': 685218, 'vols': 48952.32511039801}, {'amounts': 198825589.71645743, 'currency': 'zlabtc', 'counts': 264495, 'vols': 4626.788361149962}, {'amounts': 350247900.3655342, 'currency': 'abtbtc', 'counts': 493050, 'vols': 35644.45860853284}, {'amounts': 76811044.79237814, 'currency': 'mtxbtc', 'counts': 381454, 'vols': 6561.174356171409}, {'amounts': 23723732.284806523, 'currency': 'nasbtc', 'counts': 638481, 'vols': 16587.634886226817}, {'amounts': 29177616.439419635, 'currency': 'venbtc', 'counts': 430200, 'vols': 11602.88410393896}, {'amounts': 6791500410.4170065, 'currency': 'dtabtc', 'counts': 414032, 'vols': 10308.137520551723}, {'amounts': 1625272.4947047818, 'currency': 'neobtc', 'counts': 390284, 'vols': 12688.63967853195}, {'amounts': 217571482.42976177, 'currency': 'waxbtc', 'counts': 362939, 'vols': 6600.914331289164}, {'amounts': 337305974.59018373, 'currency': 'btsbtc', 'counts': 345740, 'vols': 8529.818229907454}, {'amounts': 2151799682.566943, 'currency': 'zilbtc', 'counts': 460850, 'vols': 16381.127103449237}, {'amounts': 538312290.2547107, 'currency': 'thetabtc', 'counts': 351684, 'vols': 8510.147341325974}, {'amounts': 543481882.5229617, 'currency': 'ctxcbtc', 'counts': 903796, 'vols': 57921.53952151358}, {'amounts': 123742590.25259466, 'currency': 'srnbtc', 'counts': 299483, 'vols': 5084.365305070205}, {'amounts': 147793748.93031392, 'currency': 'xembtc', 'counts': 366998, 'vols': 5490.969946070242}, {'amounts': 8601809866.483082, 'currency': 'edubtc', 'counts': 380621, 'vols': 2911.7394051870297}, {'amounts': 19484588.2172251, 'currency': 'icxbtc', 'counts': 355832, 'vols': 6855.693989599793}, {'amounts': 332718.6344061795, 'currency': 'dgdbtc', 'counts': 361325, 'vols': 10413.27382254797}, {'amounts': 352384170.5203864, 'currency': 'chatbtc', 'counts': 408043, 'vols': 4286.386617231527}, {'amounts': 472622242.19418895, 'currency': 'wprbtc', 'counts': 336451, 'vols': 6564.766733157525}, {'amounts': 2557629.269962485, 'currency': 'lunbtc', 'counts': 235377, 'vols': 3294.9146853293687}, {'amounts': 4670675597.169003, 'currency': 'swftcbtc', 'counts': 204506, 'vols': 6656.336797868412}, {'amounts': 680293220.4887145, 'currency': 'sntbtc', 'counts': 412352, 'vols': 9725.361091108318}, {'amounts': 2598898792.180847, 'currency': 'meetbtc', 'counts': 324745, 'vols': 15400.667237010164}, {'amounts': 6392215523.778607, 'currency': 'yeebtc', 'counts': 1070217, 'vols': 11181.482864276202}, {'amounts': 496057865.5034865, 'currency': 'elfbtc', 'counts': 603324, 'vols': 53745.23927136202}, {'amounts': 1214726565.0389352, 'currency': 'letbtc', 'counts': 340590, 'vols': 6643.547168638123}, {'amounts': 5216432.424727272, 'currency': 'qtumbtc', 'counts': 413399, 'vols': 10773.72300706796}, {'amounts': 4126100.139114591, 'currency': 'lskbtc', 'counts': 338612, 'vols': 5140.120704691285}, {'amounts': 110800411.0333569, 'currency': 'itcbtc', 'counts': 528557, 'vols': 15836.121100535263}, {'amounts': 1828042200.5074973, 'currency': 'socbtc', 'counts': 415915, 'vols': 7946.8179675660085}, {'amounts': 73815064.50214992, 'currency': 'qashbtc', 'counts': 207612, 'vols': 6038.816582193731}, {'amounts': 845873026.0292982, 'currency': 'mdsbtc', 'counts': 510329, 'vols': 9738.407447509253}, {'amounts': 1256485766.9337668, 'currency': 'ekobtc', 'counts': 335992, 'vols': 5785.348535165657}, {'amounts': 1544618202.8808687, 'currency': 'topcbtc', 'counts': 326966, 'vols': 4893.847175390369}, {'amounts': 803286893.9386023, 'currency': 'mtnbtc', 'counts': 380119, 'vols': 10630.868844214358}, {'amounts': 696002504.3788997, 'currency': 'actbtc', 'counts': 512441, 'vols': 21336.366480743676}, {'amounts': 11711636.470905136, 'currency': 'hsrbtc', 'counts': 443483, 'vols': 10220.064905998115}, {'amounts': 700612766.5338539, 'currency': 'stkbtc', 'counts': 316854, 'vols': 4905.60343575919}, {'amounts': 87586791.26860245, 'currency': 'storjbtc', 'counts': 384508, 'vols': 9924.917242851958}, {'amounts': 140288760.9754322, 'currency': 'gnxbtc', 'counts': 315323, 'vols': 7172.332515645863}, {'amounts': 784611647.47265, 'currency': 'dbcbtc', 'counts': 365827, 'vols': 5249.304730446734}, {'amounts': 209259818.0461808, 'currency': 'sncbtc', 'counts': 343560, 'vols': 4857.964113112769}, {'amounts': 1565742247.050056, 'currency': 'cmtbtc', 'counts': 391489, 'vols': 22122.77968781474}, {'amounts': 998901354.6051571, 'currency': 'tnbbtc', 'counts': 221988, 'vols': 4703.957540075545}, {'amounts': 1061196523.5597954, 'currency': 'ruffbtc', 'counts': 368271, 'vols': 9181.341778246679}, {'amounts': 1452061804.2965968, 'currency': 'qunbtc', 'counts': 421816, 'vols': 5501.052248616335}, {'amounts': 66978491.06353935, 'currency': 'zrxbtc', 'counts': 171207, 'vols': 6190.354540618775}, {'amounts': 105793149.05407043, 'currency': 'kncbtc', 'counts': 307662, 'vols': 18186.160180140294}, {'amounts': 127484595.32157649, 'currency': 'blzbtc', 'counts': 362755, 'vols': 6521.208052901578}, {'amounts': 156368096.6323268, 'currency': 'propybtc', 'counts': 303748, 'vols': 24008.02269274325}, {'amounts': 322980932.8994142, 'currency': 'rpxbtc', 'counts': 305260, 'vols': 3568.8345296241673}, {'amounts': 65112370.49045912, 'currency': 'appcbtc', 'counts': 338554, 'vols': 3523.5846839584337}, {'amounts': 929423936.2936982, 'currency': 'aidocbtc', 'counts': 481441, 'vols': 4842.955298438521}, {'amounts': 95402716.0893071, 'currency': 'powrbtc', 'counts': 169045, 'vols': 4642.606292247558}, {'amounts': 192720934.08731532, 'currency': 'cvcbtc', 'counts': 381740, 'vols': 7026.522028609736}, {'amounts': 47201044.590807386, 'currency': 'paybtc', 'counts': 329012, 'vols': 6863.982034518351}, {'amounts': 367071718.44713664, 'currency': 'qspbtc', 'counts': 323234, 'vols': 6381.791689855242}, {'amounts': 1162593924.2489257, 'currency': 'datbtc', 'counts': 321156, 'vols': 4192.125681640904}, {'amounts': 53990800.616365455, 'currency': 'rdnbtc', 'counts': 340952, 'vols': 10834.020482014123}, {'amounts': 7323376.130667318, 'currency': 'mcobtc', 'counts': 332437, 'vols': 7501.6599765688225}, {'amounts': 504222691.7761602, 'currency': 'rcnbtc', 'counts': 348563, 'vols': 6991.9851697124595}, {'amounts': 576650800.858873, 'currency': 'manabtc', 'counts': 329934, 'vols': 7033.188402176576}, {'amounts': 184968365.97447523, 'currency': 'utkbtc', 'counts': 310331, 'vols': 3676.337955245403}, {'amounts': 445906206.85004157, 'currency': 'tntbtc', 'counts': 175660, 'vols': 5082.6213166586895}, {'amounts': 2592744.2850896865, 'currency': 'gasbtc', 'counts': 319553, 'vols': 6251.005296410168}, {'amounts': 167102545.18116647, 'currency': 'batbtc', 'counts': 320633, 'vols': 5596.588130568996}, {'amounts': 149366836.57693493, 'currency': 'ostbtc', 'counts': 319973, 'vols': 3458.0131219585905}, {'amounts': 87907609.13066581, 'currency': 'linkbtc', 'counts': 319367, 'vols': 4141.6480339722775}, {'amounts': 233369375.27334082, 'currency': 'gntbtc', 'counts': 424459, 'vols': 10637.129807136243}, {'amounts': 17007784.815473605, 'currency': 'mtlbtc', 'counts': 316353, 'vols': 8441.99262341521}, {'amounts': 25218497.28146694, 'currency': 'evxbtc', 'counts': 321295, 'vols': 3986.1083386196997}, {'amounts': 165738375.78719482, 'currency': 'reqbtc', 'counts': 158797, 'vols': 4034.241395381095}, {'amounts': 49808506.49988703, 'currency': 'adxbtc', 'counts': 364681, 'vols': 4772.373611421034}, {'amounts': 122472592.37837839, 'currency': 'astbtc', 'counts': 175767, 'vols': 5587.468565899097}, {'amounts': 22334994.43856639, 'currency': 'engbtc', 'counts': 335130, 'vols': 5043.390438693633}, {'amounts': 15581070.063683357, 'currency': 'saltbtc', 'counts': 339089, 'vols': 5214.703125051081}, {'amounts': 97094665.48775832, 'currency': 'bifibtc', 'counts': 25057, 'vols': 333.057295767407}, {'amounts': 547825276.4499799, 'currency': 'bcxbtc', 'counts': 30509, 'vols': 884.1348650501426}, {'amounts': 353215.64722488075, 'currency': 'bcdbtc', 'counts': 10692, 'vols': 300.27867623527965}, {'amounts': 64176.96092153743, 'currency': 'sbtcbtc', 'counts': 9534, 'vols': 239.69396372990585}, {'amounts': 42718.865179288914, 'currency': 'btgbtc', 'counts': 11378, 'vols': 311.9252366399643}, {'amounts': 43540513.86808008, 'currency': 'eoseth', 'counts': 671327, 'vols': 779844.5806473744}, {'amounts': 4902854.896295245, 'currency': 'omgeth', 'counts': 283832, 'vols': 123797.78254046032}, {'amounts': 85707472.44850117, 'currency': 'adaeth', 'counts': 78622, 'vols': 39999.946937549634}, {'amounts': 30940324.05894013, 'currency': 'zrxeth', 'counts': 91521, 'vols': 47433.865487670766}, {'amounts': 65115620.96955247, 'currency': 'asteth', 'counts': 95028, 'vols': 50729.01795370498}, {'amounts': 45826937.71439761, 'currency': 'knceth', 'counts': 154516, 'vols': 126753.07977644126}, {'amounts': 62733174.726576224, 'currency': 'onteth', 'counts': 468260, 'vols': 441596.6491277528}, {'amounts': 390328487.3565717, 'currency': 'hteth', 'counts': 481316, 'vols': 1569199.8598507708}, {'amounts': 246766658.09916633, 'currency': 'btmeth', 'counts': 728137, 'vols': 371277.39904309314}, {'amounts': 2550803618.2672086, 'currency': 'iosteth', 'counts': 463675, 'vols': 182926.46575162368}, {'amounts': 4911097.899002443, 'currency': 'elaeth', 'counts': 574932, 'vols': 366774.4718064184}, {'amounts': 14825864007.142601, 'currency': 'trxeth', 'counts': 432305, 'vols': 1351501.846909123}, {'amounts': 647255153.8895956, 'currency': 'abteth', 'counts': 532078, 'vols': 1075963.1634060708}, {'amounts': 25949885.9672605, 'currency': 'naseth', 'counts': 679563, 'vols': 276151.89556254254}, {'amounts': 18149265459.86762, 'currency': 'ocneth', 'counts': 650897, 'vols': 452947.14729177224}, {'amounts': 111128713.43420744, 'currency': 'wicceth', 'counts': 251754, 'vols': 170100.53970811047}, {'amounts': 1961852827.8776464, 'currency': 'zileth', 'counts': 539617, 'vols': 233535.13483668037}, {'amounts': 464987879.75409746, 'currency': 'ctxceth', 'counts': 679263, 'vols': 799580.8613539241}, {'amounts': 154264438.02003297, 'currency': 'zlaeth', 'counts': 233592, 'vols': 57036.00791146393}, {'amounts': 450076113.3239608, 'currency': 'wpreth', 'counts': 325553, 'vols': 101168.78587707873}, {'amounts': 6028741494.501281, 'currency': 'dtaeth', 'counts': 369641, 'vols': 146825.53536192785}, {'amounts': 63232829.29761172, 'currency': 'mtxeth', 'counts': 341432, 'vols': 87874.28600921841}, {'amounts': 486091534.9532822, 'currency': 'thetaeth', 'counts': 344696, 'vols': 125036.99406201829}, {'amounts': 76187393.73175637, 'currency': 'srneth', 'counts': 242762, 'vols': 49307.5701755363}, {'amounts': 24375745.736989807, 'currency': 'veneth', 'counts': 371911, 'vols': 157525.94457901246}, {'amounts': 253565793.09453884, 'currency': 'btseth', 'counts': 298745, 'vols': 100025.42066912724}, {'amounts': 11718017693.961075, 'currency': 'edueth', 'counts': 369874, 'vols': 62124.55441340578}, {'amounts': 146845190.655287, 'currency': 'waxeth', 'counts': 293999, 'vols': 67594.48009916503}, {'amounts': 8604906.046685148, 'currency': 'hsreth', 'counts': 341352, 'vols': 118478.52749204636}, {'amounts': 15828073.606502512, 'currency': 'icxeth', 'counts': 319184, 'vols': 88689.92456221308}, {'amounts': 1014513449.8346772, 'currency': 'mtneth', 'counts': 367308, 'vols': 218626.20538642662}, {'amounts': 883868845.2557544, 'currency': 'acteth', 'counts': 449474, 'vols': 404397.1613032058}, {'amounts': 118429340.57259367, 'currency': 'blzeth', 'counts': 344210, 'vols': 97523.86355319292}, {'amounts': 66907298.03771691, 'currency': 'qasheth', 'counts': 199427, 'vols': 89136.3303305436}, {'amounts': 986326100.6024543, 'currency': 'ruffeth', 'counts': 344900, 'vols': 136886.13256460868}, {'amounts': 2139822661.7600331, 'currency': 'cmteth', 'counts': 399168, 'vols': 478233.76527630293}, {'amounts': 176388498.44397974, 'currency': 'elfeth', 'counts': 514210, 'vols': 305720.5202830469}, {'amounts': 1008248059.6050098, 'currency': 'meeteth', 'counts': 313576, 'vols': 95502.31890401978}, {'amounts': 1328731988.621833, 'currency': 'soceth', 'counts': 351841, 'vols': 89505.9596487541}, {'amounts': 3895775.04709768, 'currency': 'qtumeth', 'counts': 343099, 'vols': 130901.99027677659}, {'amounts': 64305638.37284438, 'currency': 'itceth', 'counts': 344005, 'vols': 146123.02366838593}, {'amounts': 3772124911.1528816, 'currency': 'swftceth', 'counts': 179258, 'vols': 81656.50520667218}, {'amounts': 5093392368.991548, 'currency': 'yeeeth', 'counts': 934035, 'vols': 134997.6313278532}, {'amounts': 3618958.4639449706, 'currency': 'lsketh', 'counts': 318698, 'vols': 73460.90511934737}, {'amounts': 1694344.317458475, 'currency': 'luneth', 'counts': 204602, 'vols': 35172.030863167405}, {'amounts': 1155228446.5623076, 'currency': 'leteth', 'counts': 319200, 'vols': 102373.04335148772}, {'amounts': 129648047.01611587, 'currency': 'gnxeth', 'counts': 311106, 'vols': 108378.04866332475}, {'amounts': 256045820.18636262, 'currency': 'chateth', 'counts': 349530, 'vols': 48583.776706964694}, {'amounts': 1095907234.195146, 'currency': 'ekoeth', 'counts': 315054, 'vols': 81624.10892866172}, {'amounts': 1905640876.299624, 'currency': 'topceth', 'counts': 376449, 'vols': 97015.82179182522}, {'amounts': 294166.16904664587, 'currency': 'dgdeth', 'counts': 331952, 'vols': 150432.40048664715}, {'amounts': 689057931.3330413, 'currency': 'stketh', 'counts': 320057, 'vols': 77652.75631011405}, {'amounts': 834741085.25831, 'currency': 'mdseth', 'counts': 489396, 'vols': 156320.30343503415}, {'amounts': 703118276.6784408, 'currency': 'dbceth', 'counts': 344131, 'vols': 74155.64144781837}, {'amounts': 197916305.44644856, 'currency': 'snceth', 'counts': 325275, 'vols': 74745.00074438944}, {'amounts': 43159213.926908225, 'currency': 'payeth', 'counts': 307581, 'vols': 102041.41849704745}, {'amounts': 1513398070.05601, 'currency': 'quneth', 'counts': 408107, 'vols': 92337.10394631387}, {'amounts': 716560445.3528081, 'currency': 'aidoceth', 'counts': 395189, 'vols': 59500.70394808433}, {'amounts': 905201519.2725623, 'currency': 'tnbeth', 'counts': 184039, 'vols': 66720.06469191275}, {'amounts': 53479787.04055891, 'currency': 'appceth', 'counts': 303390, 'vols': 46091.67483216941}, {'amounts': 51842632.89719964, 'currency': 'rdneth', 'counts': 323672, 'vols': 168828.67995724187}, {'amounts': 178808938.67923802, 'currency': 'utketh', 'counts': 310627, 'vols': 57946.19577740826}, {'amounts': 87465148.65899613, 'currency': 'powreth', 'counts': 151513, 'vols': 69036.82659239396}, {'amounts': 157305677.72818255, 'currency': 'bateth', 'counts': 300947, 'vols': 84452.43250101461}, {'amounts': 68067568.38608782, 'currency': 'propyeth', 'counts': 279724, 'vols': 161306.96489619056}, {'amounts': 501092806.69832957, 'currency': 'manaeth', 'counts': 310596, 'vols': 95538.39299463206}, {'amounts': 156576023.71303755, 'currency': 'reqeth', 'counts': 149833, 'vols': 61916.21359284062}, {'amounts': 167289720.57523444, 'currency': 'cvceth', 'counts': 323974, 'vols': 97520.27704452563}, {'amounts': 354658209.67548466, 'currency': 'qspeth', 'counts': 308877, 'vols': 99976.58525249938}, {'amounts': 21645791.032372046, 'currency': 'evxeth', 'counts': 302752, 'vols': 55424.65116524843}, {'amounts': 1077985829.4084084, 'currency': 'dateth', 'counts': 314032, 'vols': 61452.610589876815}, {'amounts': 6275047.633658153, 'currency': 'mcoeth', 'counts': 308103, 'vols': 93897.53830659413}, {'amounts': 179811185.53287718, 'currency': 'gnteth', 'counts': 343708, 'vols': 121004.39191406028}, {'amounts': 2486782.4473167323, 'currency': 'gaseth', 'counts': 303074, 'vols': 98066.66243561947}, {'amounts': 127717701.57827097, 'currency': 'osteth', 'counts': 306048, 'vols': 47244.956434198146}, {'amounts': 84725910.45581338, 'currency': 'linketh', 'counts': 304266, 'vols': 65595.53237739121}, {'amounts': 463875316.48388565, 'currency': 'rcneth', 'counts': 319521, 'vols': 104442.54644494964}, {'amounts': 402543882.3345814, 'currency': 'tnteth', 'counts': 157512, 'vols': 74250.25150603736}, {'amounts': 21542769.54136546, 'currency': 'engeth', 'counts': 323303, 'vols': 79046.37592197586}, {'amounts': 13908130.209093617, 'currency': 'salteth', 'counts': 314057, 'vols': 75164.51129906424}, {'amounts': 40504230.940976724, 'currency': 'adxeth', 'counts': 328393, 'vols': 61731.91735768556}]


sorted_by_amounts = sorted(obj, key=lambda x: x['amounts'], reverse=True)
pickle.dump(sorted_by_amounts, open("huobi_order_by_amounts.txt", "w"))
print("按成交量amounts排序（降序）：")
for row in sorted_by_amounts:
        print(row)
print(" ")

sorted_by_vols = sorted(obj, key=lambda x: x['vols'], reverse=True)
pickle.dump(sorted_by_vols, open("huobi_order_by_vols.txt", "w"))
print("按成交额vols排序(降序)：")
for row in sorted_by_vols:
        print(row)

sorted_by_counts = sorted(obj, key=lambda x: x['counts'], reverse=True)
pickle.dump(sorted_by_counts, open("huobi_order_by_trades.txt", "w"))
print("按成交额vols排序(降序)：")
for row in sorted_by_counts:
        print(row)