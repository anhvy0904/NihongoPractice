"""Biên soạn thẻ học cho từ vựng và mẫu ngữ pháp. Không gán cấp JLPT chính thức."""
from pathlib import Path
import json, re, sys
sys.path.insert(0,str(Path(__file__).parent/'.libraries'))
from janome.tokenizer import Tokenizer

# Từ | âm Hán Việt của chữ Hán | dịch ví dụ | gần nghĩa (từ~đọc~nghĩa) | trái nghĩa/đối chiếu
# Dấu ! trước từ: từ đối chiếu, không phải trái nghĩa trực tiếp.
ENRICH = '''貿易|mậu dịch|Nhật Bản giao thương với nhiều nước.|交易~こうえき~giao thương|!国内取引~こくないとりひき~giao dịch trong nước
輸出|thâu xuất|Công ty này xuất khẩu máy móc.|海外に売る~かいがいにうる~bán ra nước ngoài|輸入~ゆにゅう~nhập khẩu
輸入|thâu nhập|Nhập khẩu thực phẩm từ nước ngoài.|外国から買う~がいこくからかう~mua từ nước ngoài|輸出~ゆしゅつ~xuất khẩu
機能|cơ năng|Thêm chức năng mới vào ứng dụng.|働き~はたらき~chức năng, tác dụng|!性能~せいのう~hiệu năng, khả năng hoạt động
単体テスト|đơn thể|Kiểm thử riêng hàm đã triển khai.|ユニットテスト~ユニットテスト~kiểm thử đơn vị|!結合テスト~けつごうテスト~kiểm thử tích hợp
結合テスト|kết hợp|Kiểm tra sự phối hợp giữa các mô-đun bằng kiểm thử tích hợp.|統合テスト~とうごうテスト~kiểm thử tích hợp|!単体テスト~たんたいテスト~kiểm thử đơn vị
試験項目|thí nghiệm hạng mục|Tổng hợp các hạng mục kiểm thử thành danh sách.|テスト項目~テストこうもく~hạng mục kiểm thử|!試験結果~しけんけっか~kết quả kiểm thử
進捗|tiến duệ|Báo cáo tiến độ phát triển trong buổi họp sáng.|進み具合~すすみぐあい~mức độ tiến triển|!停滞~ていたい~sự đình trệ
注意点|chú ý điểm|Kiểm tra các điểm cần lưu ý trước khi bắt đầu công việc.|留意点~りゅういてん~điểm cần chú ý|!利点~りてん~ưu điểm
統一|thống nhất|Thống nhất mẫu biểu trong nhóm.|そろえる~そろえる~làm cho đồng nhất|不統一~ふとういつ~không thống nhất
予定|dự định|Kiểm tra kế hoạch ngày mai.|計画~けいかく~kế hoạch|!実績~じっせき~kết quả đã thực hiện
程度|trình độ|Thay đổi cách xử lý tùy mức độ lỗi.|度合い~どあい~mức độ|!種類~しゅるい~loại, chủng loại
朝会|triêu hội|Họp đầu giờ sáng lúc chín giờ mỗi ngày.|朝の会議~あさのかいぎ~cuộc họp buổi sáng|!終礼~しゅうれい~buổi họp cuối ngày
課題|khóa đề|Cả nhóm trao đổi về vấn đề hiện tại.|問題~もんだい~vấn đề|!解決策~かいけつさく~phương án giải quyết
開発|khai phát|Tiến hành phát triển ứng dụng mới.|作り出す~つくりだす~tạo ra|!保守~ほしゅ~bảo trì
担当|đảm đương|Người phụ trách chức năng này là anh Tanaka.|受け持ち~うけもち~phần phụ trách|!担当外~たんとうがい~ngoài phạm vi phụ trách
数字|số tự|Kiểm tra các con số trong báo cáo.|数値~すうち~giá trị số|!文字~もじ~chữ, ký tự
件数|kiện số|Đếm số lượt hỏi trong một ngày.|件の数~けんのかず~số trường hợp|!人数~にんずう~số người
消化|tiêu hóa|Đã xử lý xong toàn bộ công việc dự kiến.|こなす~こなす~xử lý, hoàn thành|!未処理~みしょり~chưa xử lý
トラブル|—|Đã xảy ra sự cố trong hệ thống.|問題~もんだい~vấn đề, rắc rối|!順調~じゅんちょう~thuận lợi
解決策|giải quyết sách|Cả nhóm suy nghĩ phương án giải quyết.|対策~たいさく~biện pháp đối phó|!原因~げんいん~nguyên nhân
遅れ|trì|Báo cáo việc chậm tiến độ.|遅延~ちえん~chậm trễ|!前倒し~まえだおし~đẩy lịch sớm lên
遅延|trì diên|Kiểm tra độ trễ truyền thông.|遅れ~おくれ~sự chậm trễ|!定刻~ていこく~đúng giờ quy định
事実|sự thực|Xác minh sự thật thay vì suy đoán.|本当のこと~ほんとうのこと~điều có thật|虚構~きょこう~hư cấu
進捗率|tiến duệ suất|Tỷ lệ hoàn thành hiện tại là tám mươi phần trăm.|完了した割合~かんりょうしたわりあい~tỷ lệ đã hoàn tất|!残りの割合~のこりのわりあい~tỷ lệ còn lại
工程|công trình|Chuyển sang công đoạn tiếp theo.|作業の手順~さぎょうのてじゅん~trình tự công việc|!工期~こうき~thời gian thi công
詳細|tường tế|Kiểm tra nội dung chi tiết của đặc tả.|詳しい内容~くわしいないよう~nội dung cụ thể|概要~がいよう~khái quát
影響|ảnh hưởng|Điều tra ảnh hưởng của thay đổi.|作用~さよう~tác động|!無関係~むかんけい~không liên quan
原因|nguyên nhân|Tìm nguyên nhân của lỗi.|理由~りゆう~lý do|!結果~けっか~kết quả
段階|đoạn giai|Việc phát triển đã bước vào giai đoạn kiểm thử.|ステップ~ステップ~bước, giai đoạn|!全体~ぜんたい~toàn bộ
不足|bất túc|Muốn giải quyết tình trạng thiếu nhân lực.|足りない~たりない~không đủ|十分~じゅうぶん~đầy đủ
主流|chủ lưu|Hiện nay phương pháp này được dùng phổ biến.|中心的な傾向~ちゅうしんてきなけいこう~xu hướng chính|傍流~ぼうりゅう~nhánh phụ, xu hướng phụ
難易度|nan dị độ|Kiểm tra mức độ khó dễ của nhiệm vụ.|難しさ~むずかしさ~độ khó|!容易~ようい~dễ dàng
規模|quy mô|Dự án có quy mô lớn.|大きさ~おおきさ~độ lớn|!範囲~はんい~phạm vi
状態|trạng thái|Kiểm tra trạng thái thiết bị.|様子~ようす~tình trạng|!変化~へんか~sự thay đổi
作業|tác nghiệp|Bắt đầu công việc hôm nay.|仕事~しごと~công việc|!休憩~きゅうけい~nghỉ giải lao
余裕|dư dụ|Vẫn còn dư thời gian trước hạn chót.|ゆとり~ゆとり~sự dư dả|!切迫~せっぱく~tình trạng cấp bách
最善|tối thiện|Chọn phương pháp tốt nhất.|ベスト~ベスト~tốt nhất|最悪~さいあく~tệ nhất
締め切り|đế; thiết|Hạn nộp báo cáo là thứ Sáu.|期限~きげん~thời hạn|!開始~かいし~bắt đầu
直前|trực tiền|Kiểm tra tài liệu ngay trước cuộc họp.|すぐ前~すぐまえ~ngay trước|直後~ちょくご~ngay sau
遅刻|trì khắc|Vì ngủ dậy muộn nên đến công ty trễ.|遅れて来る~おくれてくる~đến muộn|!早退~そうたい~về sớm
部署|bộ thự|Từ tháng sau tôi làm ở bộ phận khác.|部門~ぶもん~phòng ban|!会社全体~かいしゃぜんたい~toàn công ty
資料|tư liệu|Chuẩn bị tài liệu cuộc họp.|文書~ぶんしょ~văn bản, tài liệu|!口頭説明~こうとうせつめい~giải thích bằng lời nói
導入|đạo nhập|Cân nhắc đưa công cụ mới vào sử dụng.|取り入れる~とりいれる~đưa vào, tiếp nhận|廃止~はいし~bãi bỏ
状況|trạng huống|Báo cáo tình hình hiện tại.|様子~ようす~tình hình|!予定~よてい~kế hoạch
経験|kinh nghiệm|Anh ấy có nhiều kinh nghiệm phát triển phần mềm.|体験~たいけん~trải nghiệm|!未経験~みけいけん~chưa có kinh nghiệm
可能性|khả năng tính|Có khả năng kế hoạch sẽ thay đổi.|見込み~みこみ~khả năng, triển vọng|!不可能~ふかのう~không thể
注文する|chú văn|Đặt mua hàng cần thiết ở cửa hàng.|頼む~たのむ~yêu cầu, đặt|!キャンセルする~キャンセルする~hủy
発注する|phát chú|Đặt linh kiện từ nhà cung cấp.|注文する~ちゅうもんする~đặt hàng|!受注する~じゅちゅうする~nhận đơn hàng
管理する|quản lý|Trưởng nhóm quản lý tiến độ.|監督する~かんとくする~giám sát|!放置する~ほうちする~bỏ mặc
準備する|chuẩn bị|Chuẩn bị tài liệu cuộc họp.|用意する~よういする~chuẩn bị|!片付ける~かたづける~thu dọn
実施する|thực thi|Ngày mai tiến hành kiểm thử đơn vị.|行う~おこなう~tiến hành|!中止する~ちゅうしする~dừng, hủy
進める|tiến|Tiến hành phát triển theo kế hoạch.|推進する~すいしんする~thúc đẩy|止める~とめる~dừng
共有する|cộng hữu|Chia sẻ các điểm cần chú ý với cả nhóm.|分かち合う~わかちあう~cùng chia sẻ|独占する~どくせんする~độc chiếm
完了する|hoàn liễu|Hoàn tất công việc trong hôm nay.|終える~おえる~hoàn tất|!開始する~かいしする~bắt đầu
残業する|tàn nghiệp|Hôm nay làm thêm giờ vì gần hạn giao hàng.|時間外勤務~じかんがいきんむ~làm ngoài giờ|!定時退社~ていじたいしゃ~tan làm đúng giờ
相談する|tương đàm|Nếu gặp khó khăn thì hỏi ý kiến đàn anh.|話し合う~はなしあう~trao đổi|!独断で決める~どくだんできめる~tự quyết định
隠す|ẩn|Che giấu lỗi là không tốt.|秘密にする~ひみつにする~giữ bí mật|明かす~あかす~tiết lộ
対応する|đối ứng|Xử lý câu hỏi của khách hàng.|応じる~おうじる~đáp ứng, ứng phó|!無視する~むしする~phớt lờ
終了する|chung liễu|Cuộc họp kết thúc lúc năm giờ.|終わる~おわる~kết thúc|開始する~かいしする~bắt đầu
提出する|đề xuất|Nộp báo cáo cho thầy cô.|差し出す~さしだす~đưa ra, trình|!受け取る~うけとる~nhận
報告する|báo cáo|Báo cáo việc chậm tiến độ với trưởng nhóm.|知らせる~しらせる~thông báo|!隠す~かくす~che giấu
依存する|y tồn|Chức năng này phụ thuộc hệ thống bên ngoài.|頼る~たよる~dựa vào|自立する~じりつする~tự lập
調整する|điều chỉnh|Điều chỉnh lịch họp.|整える~ととのえる~sắp xếp cho phù hợp|!乱す~みだす~làm rối
回避する|hồi tị|Tránh sự cố bằng cách kiểm tra trước.|避ける~さける~tránh|!直面する~ちょくめんする~đối mặt
調査する|điều tra|Điều tra nguyên nhân của lỗi.|調べる~しらべる~tìm hiểu|!推測する~すいそくする~suy đoán
取り戻す|thủ; lệ|Lấy lại dữ liệu từ bản sao lưu.|回復する~かいふくする~khôi phục|失う~うしなう~mất
限る|hạn|Giới hạn số người tham gia là mười người.|限定する~げんていする~giới hạn|!広げる~ひろげる~mở rộng
進行する|tiến hành|Cuộc họp diễn ra theo kế hoạch.|進む~すすむ~tiến triển|停止する~ていしする~dừng lại
増員する|tăng viên|Tăng nhân sự vì công việc nhiều hơn.|人数を増やす~にんずうをふやす~tăng số người|減員する~げんいんする~giảm nhân sự
統計する|thống kế|Thống kê số vụ mỗi tháng.|集計する~しゅうけいする~tổng hợp số liệu|!個別に見る~こべつにみる~xem từng trường hợp
出荷する|xuất hà|Xuất hàng khách đã đặt.|発送する~はっそうする~gửi hàng đi|!入荷する~にゅうかする~hàng nhập kho
編集する|biên tập|Biên tập đoạn video đã quay.|構成し直す~こうせいしなおす~sắp xếp lại nội dung|!撮影する~さつえいする~quay phim, chụp ảnh
返品する|phản phẩm|Trả lại món hàng bị hỏng.|商品を返す~しょうひんをかえす~trả lại hàng|!購入する~こうにゅうする~mua hàng
慌てる|hoảng|Không cần hốt hoảng khi có lỗi.|うろたえる~うろたえる~luống cuống|落ち着く~おちつく~bình tĩnh
提案する|đề án|Đề xuất phương pháp mới.|案を出す~あんをだす~đưa ra phương án|!却下する~きゃっかする~bác bỏ
連携する|liên huề|Hai bộ phận phối hợp với nhau.|協力する~きょうりょくする~hợp tác|!単独で行う~たんどくでおこなう~thực hiện riêng lẻ
支援する|chi viện|Công ty hỗ trợ việc học của nhân viên mới.|援助する~えんじょする~giúp đỡ|妨害する~ぼうがいする~cản trở
修正する|tu chính|Sửa lỗi trong mã chương trình.|訂正する~ていせいする~sửa lại|!改悪する~かいあくする~sửa thành tệ hơn
検討する|kiểm thảo|Xem xét việc đưa công cụ mới vào sử dụng.|考慮する~こうりょする~cân nhắc|!即決する~そっけつする~quyết định ngay
頼む|lại|Nhờ đàn anh kiểm tra.|依頼する~いらいする~nhờ, yêu cầu|!断る~ことわる~từ chối
追加する|truy gia|Thêm hạng mục kiểm thử.|加える~くわえる~thêm vào|削除する~さくじょする~xóa bỏ
加える|gia|Thêm phần giải thích vào tài liệu.|足す~たす~thêm|除く~のぞく~loại bỏ
個性的|cá tính đích|Thiết kế của anh ấy có nét riêng.|独特~どくとく~độc đáo|平凡~へいぼん~tầm thường
具体的|cụ thể đích|Nghĩ ra phương án giải quyết cụ thể.|明確~めいかく~rõ ràng|抽象的~ちゅうしょうてき~trừu tượng
順調|thuận điều|Công việc tiến triển thuận lợi.|順調に進む~じゅんちょうにすすむ~tiến triển tốt|不調~ふちょう~không tốt, trục trặc
技術的|kỹ thuật đích|Điều tra vấn đề kỹ thuật.|技術に関する~ぎじゅつにかんする~liên quan kỹ thuật|!事務的~じむてき~về hành chính
重要|trọng yếu|Đây là điểm lưu ý quan trọng.|大切~たいせつ~quan trọng|!些細~ささい~nhỏ nhặt
正確|chính xác|Báo cáo số liệu chính xác.|的確~てきかく~chính xác, trúng|不正確~ふせいかく~không chính xác
複雑|phức tạp|Chức năng này phức tạp.|込み入った~こみいった~rắc rối, phức tạp|単純~たんじゅん~đơn giản
重大|trọng đại|Đã phát hiện lỗi nghiêm trọng.|深刻~しんこく~nghiêm trọng|軽微~けいび~nhẹ, nhỏ
普通|phổ thông|Không có vấn đề nếu sử dụng bình thường.|一般的~いっぱんてき~thông thường|特別~とくべつ~đặc biệt
簡単|giản đơn|Đây là công việc đơn giản.|容易~ようい~dễ dàng|難しい~むずかしい~khó
適当|thích đương|Chọn phương pháp phù hợp với mục đích.|適切~てきせつ~thích hợp|不適当~ふてきとう~không phù hợp
正直に|chính trực|Nếu có vấn đề, hãy báo cáo thành thật.|素直に~すなおに~thẳng thắn, thật lòng|!うそをついて~うそをついて~nói dối
早めに|tảo|Nộp tài liệu sớm một chút.|前もって~まえもって~trước, từ trước|!遅めに~おそめに~muộn hơn một chút
速やかに|tốc|Xử lý sự cố nhanh chóng.|迅速に~じんそくに~nhanh chóng|!ゆっくり~ゆっくり~chậm rãi
すぐに|—|Việc không hiểu thì hỏi ngay.|直ちに~ただちに~ngay lập tức|!後で~あとで~sau đó
ゆっくり|—|Hãy đọc phần giải thích chậm rãi.|のんびり~のんびり~thong thả|急いで~いそいで~vội vàng
たまに|—|Anh ấy thỉnh thoảng làm thêm giờ.|時々~ときどき~đôi khi|頻繁に~ひんぱんに~thường xuyên
時々|thời|Lỗi này thỉnh thoảng xảy ra.|時折~ときおり~thỉnh thoảng|いつも~いつも~luôn luôn
しっかり|—|Kiểm tra kỹ các yêu cầu.|きちんと~きちんと~cẩn thận, đúng cách|!いい加減に~いいかげんに~qua loa
なるべく|—|Hãy báo cáo càng sớm càng tốt.|できるだけ~できるだけ~trong khả năng có thể|!必ず~かならず~nhất định, bắt buộc
やっと|—|Cuối cùng đợt kiểm thử dài cũng kết thúc.|ようやく~ようやく~cuối cùng cũng|!まだ~まだ~vẫn chưa
たぶん|—|Có lẽ đến ngày mai sẽ hoàn tất.|おそらく~おそらく~có lẽ|!確実に~かくじつに~chắc chắn
わざと|—|Cố ý tạo lỗi để kiểm tra.|故意に~こいに~cố ý|偶然に~ぐうぜんに~ngẫu nhiên
タイミング|—|Cân nhắc thời điểm báo cáo.|時機~じき~thời điểm thích hợp|!時刻~じこく~giờ cụ thể
コーディング|—|Bắt đầu viết mã sau khi thiết kế.|コードを書く~コードをかく~viết mã|!設計~せっけい~thiết kế
ロジック|—|Kiểm tra logic tính toán.|論理~ろんり~logic, lý luận|!矛盾~むじゅん~mâu thuẫn
リーダー|—|Trưởng nhóm phân công công việc.|指導者~しどうしゃ~người lãnh đạo|!部下~ぶか~cấp dưới
メンバー|—|Trao đổi với thành viên trong nhóm.|一員~いちいん~một thành viên|!部外者~ぶがいしゃ~người ngoài
プログラム|—|Chạy chương trình mới.|ソフトウェア~ソフトウェア~phần mềm (khái niệm rộng hơn)|!ハードウェア~ハードウェア~phần cứng
チーム|—|Chia sẻ thông tin trong nhóm.|グループ~グループ~nhóm|!個人~こじん~cá nhân
エラー|—|Kiểm tra lỗi nhập liệu.|誤り~あやまり~lỗi, sai sót|!正常~せいじょう~bình thường, đúng
クレーム|—|Xử lý khiếu nại của khách hàng.|苦情~くじょう~lời phàn nàn|!感謝~かんしゃ~lòng biết ơn
バグ|—|Phát hiện lỗi qua kiểm thử.|不具合~ふぐあい~trục trặc|!正常動作~せいじょうどうさ~hoạt động bình thường
ツール|—|Đưa công cụ tiện lợi vào sử dụng.|道具~どうぐ~công cụ|!手作業~てさぎょう~thao tác thủ công
モジュール|—|Kết hợp hai mô-đun.|構成部品~こうせいぶひん~thành phần cấu tạo|!全体~ぜんたい~toàn bộ'''

# Từ bổ sung trong Unit 9–12: từ | đọc | nghĩa | ví dụ | âm Hán Việt | dịch | gần nghĩa | đối nghĩa
EXTRA = '''処理|しょり|xử lý|コンピューターが大量のデータを処理する。|xử lý|Máy tính xử lý lượng lớn dữ liệu.|処置~しょち~xử trí (thường cho vấn đề, tình huống)|!放置~ほうち~bỏ mặc
発見|はっけん|phát hiện|新しいバグを発見した。|phát kiến|Đã phát hiện lỗi mới.|見つける~みつける~tìm thấy|!見落とす~みおとす~bỏ sót
動作|どうさ|hoạt động, vận hành|アプリが正常に動作している。|động tác|Ứng dụng đang hoạt động bình thường.|作動~さどう~hoạt động (máy móc)|!停止~ていし~dừng
傾向|けいこう|xu hướng|最近、エラーが増える傾向がある。|khuynh hướng|Gần đây có xu hướng tăng lỗi.|傾き~かたむき~khuynh hướng|!例外~れいがい~ngoại lệ
比較する|ひかくする|so sánh|二つの結果を比較する。|tỉ giảo|So sánh hai kết quả.|比べる~くらべる~so sánh|!同一視する~どういつしする~coi là một
例外|れいがい|ngoại lệ|このルールには例外がある。|lệ ngoại|Quy tắc này có ngoại lệ.|特例~とくれい~trường hợp đặc biệt|!原則~げんそく~nguyên tắc
用いる|もちいる|sử dụng (văn viết)|計算にはコンピューターを用いる。|dụng|Dùng máy tính để tính toán.|使う~つかう~dùng|!使わない~つかわない~không dùng
取り除く|とりのぞく|loại bỏ|不要なコードを取り除く。|thủ; trừ|Loại bỏ mã không cần thiết.|除去する~じょきょする~loại bỏ|加える~くわえる~thêm vào
単純|たんじゅん|đơn giản, không phức tạp|この問題は単純だ。|đơn thuần|Vấn đề này đơn giản.|簡単~かんたん~đơn giản, dễ|複雑~ふくざつ~phức tạp
落とす|おとす|làm rơi; làm mất dữ liệu|誤ってデータを落としてしまった。|lạc|Đã vô tình làm mất dữ liệu.|失う~うしなう~đánh mất|!保存する~ほぞんする~lưu lại
落ちる|おちる|rơi; phần mềm bị sập|実行中にソフトが落ちた。|lạc|Phần mềm bị sập trong lúc chạy.|異常終了する~いじょうしゅうりょうする~kết thúc bất thường|!正常に動く~せいじょうにうごく~chạy bình thường
割り当てる|わりあてる|phân công, phân bổ|リーダーは作業をメンバーに割り当てた。|cát; đương|Trưởng nhóm phân công việc cho các thành viên.|配分する~はいぶんする~phân bổ|!回収する~かいしゅうする~thu hồi
固まる|かたまる|đông cứng; máy bị đơ|パソコンが固まって操作できなくなった。|cố|Máy tính bị đơ và không thể thao tác.|フリーズする~フリーズする~bị đơ|!動く~うごく~hoạt động
参考書|さんこうしょ|sách tham khảo|参考書で文法を調べる。|tham khảo thư|Tra ngữ pháp trong sách tham khảo.|参考資料~さんこうしりょう~tài liệu tham khảo|!教科書~きょうかしょ~sách giáo khoa
改善策|かいぜんさく|biện pháp cải thiện|品質を上げる改善策を考える。|cải thiện sách|Nghĩ ra biện pháp nâng cao chất lượng.|対策~たいさく~biện pháp đối phó|!悪化~あっか~xấu đi
客観的|きゃっかんてき|khách quan|事実に基づいて客観的に判断する。|khách quan đích|Đánh giá khách quan dựa trên sự thật.|公平~こうへい~công bằng|主観的~しゅかんてき~chủ quan
助言|じょげん|lời khuyên|先輩に助言を求める。|trợ ngôn|Xin lời khuyên của đàn anh.|アドバイス~アドバイス~lời khuyên|!命令~めいれい~mệnh lệnh
外す|はずす|tháo, loại khỏi danh sách|参加者リストから名前を外す。|ngoại|Loại tên khỏi danh sách người tham gia.|取り外す~とりはずす~tháo ra|付ける~つける~gắn vào
寝坊|ねぼう|ngủ dậy muộn|寝坊したので授業に遅刻した。|tẩm phường|Vì ngủ dậy muộn nên đến lớp trễ.|朝寝坊~あさねぼう~ngủ dậy muộn|早起き~はやおき~dậy sớm
延ばす|のばす|gia hạn, hoãn|締め切りを一日延ばした。|diên|Đã gia hạn một ngày.|延期する~えんきする~hoãn|早める~はやめる~đẩy sớm lên
インストール|インストール|cài đặt phần mềm|新しいアプリをインストールした。|—|Đã cài ứng dụng mới.|導入する~どうにゅうする~đưa vào sử dụng|アンインストール~アンインストール~gỡ cài đặt
上がる|あがる|tăng lên; hoàn thành trong ngữ cảnh công việc|新しいシステムが上がったので、テストを始めた。|thượng|Hệ thống mới đã hoàn thành nên bắt đầu kiểm thử.|完成する~かんせいする~hoàn thành (ngữ cảnh này)|!未完成~みかんせい~chưa hoàn thành
きつい|きつい|chật; khắc nghiệt, vất vả|このズボンはきつくてはけない。|—|Chiếc quần này chật nên không mặc được.|窮屈~きゅうくつ~chật chội|緩い~ゆるい~rộng, lỏng
買掛金|かいかけきん|khoản phải trả nhà cung cấp do mua chịu|月末に仕入先へ買掛金を支払う。|mãi quải kim|Trả khoản nợ mua hàng cho nhà cung cấp vào cuối tháng.|未払いの仕入代金~みばらいのしいれだいきん~tiền mua hàng chưa trả|!売掛金~うりかけきん~khoản phải thu do bán chịu
手元|てもと|trong tay, bên mình|手元にある資料を使う。|thủ nguyên|Dùng tài liệu đang có trong tay.|手近~てぢか~gần tầm tay|!遠く~とおく~ở xa
店舗|てんぽ|cửa hàng, cơ sở kinh doanh|近くの店舗を検索する。|điếm phô|Tìm cửa hàng gần đây.|店~みせ~cửa hàng|!本社~ほんしゃ~trụ sở chính
成果|せいか|thành quả|今回の成果を報告する。|thành quả|Báo cáo thành quả lần này.|実績~じっせき~kết quả đạt được|!課題~かだい~vấn đề còn cần giải quyết
決定する|けっていする|quyết định|明日の会議でリーダーを決定する。|quyết định|Quyết định trưởng nhóm trong cuộc họp ngày mai.|決める~きめる~quyết định|!保留する~ほりゅうする~tạm hoãn quyết định
実行|じっこう|thực hiện|計画を実行する。|thực hành|Thực hiện kế hoạch.|実施~じっし~tiến hành|!中止~ちゅうし~dừng, hủy
依頼する|いらいする|nhờ, yêu cầu thực hiện|この仕事は専門家に依頼する。|y lại|Nhờ chuyên gia làm công việc này.|頼む~たのむ~nhờ|!断る~ことわる~từ chối
同様|どうよう|giống, tương tự|去年と同様にイベントを開催する。|đồng dạng|Tổ chức sự kiện giống năm ngoái.|同じ~おなじ~giống nhau|異なる~ことなる~khác nhau
繰り返す|くりかえす|lặp lại|重要なポイントを繰り返して説明する。|sào; phản|Giải thích lặp lại các điểm quan trọng.|反復する~はんぷくする~lặp lại|!一度だけ~いちどだけ~chỉ một lần
身につける|みにつける|học được kỹ năng; mang trên người|仕事に必要な技術を身につける。|thân|Học được kỹ năng cần thiết cho công việc.|習得する~しゅうとくする~tiếp thu, học được|!忘れる~わすれる~quên
完成する|かんせいする|hoàn thành|新しいシステムが完成した。|hoàn thành|Hệ thống mới đã hoàn thành.|出来上がる~できあがる~hoàn tất|!着手する~ちゃくしゅする~bắt tay làm'''

# Mẫu | nghĩa | cấu trúc | ví dụ | dịch | gần nghĩa | đối chiếu
GRAMMAR = '''〜せいで|vì… nên (kết quả xấu)|Nの／V・イA thể thường／ナAな + せいで|寝坊したせいで、授業に遅刻した。|Vì ngủ dậy muộn nên đến lớp trễ.|〜ために~ために~do, vì (trung tính)|!〜おかげで~おかげで~nhờ (kết quả tốt)
〜おかげで|nhờ… (kết quả tốt)|Nの／V・イA thể thường／ナAな + おかげで|先生のおかげで、試験に合格できた。|Nhờ thầy cô mà tôi đỗ kỳ thi.|〜ために~ために~do, vì (trung tính)|!〜せいで~せいで~vì (kết quả xấu)
〜ごとに|mỗi…, cứ mỗi…|N／V từ điển + ごとに|一か月ごとに、進捗を確認する。|Kiểm tra tiến độ mỗi tháng.|〜たびに~たびに~mỗi lần|!〜おきに~おきに~cách mỗi khoảng (cách dùng cần phân biệt)
〜さえ|ngay cả; chỉ cần…|N + さえ／Nさえ + Vば|時間さえあれば、参加できます。|Chỉ cần có thời gian thì tôi có thể tham gia.|〜でも~でも~ngay cả|!〜だけ~だけ~chỉ (không có sắc thái nhấn mạnh bất ngờ)
〜一方で|một mặt… mặt khác…|V・イA thể thường／ナAな／Nである + 一方で|この道具は便利な一方で、値段が高い。|Công cụ này tiện lợi nhưng giá cao.|〜反面~はんめん~mặt khác, trái lại|!〜だけでなく~だけでなく~không chỉ (bổ sung)
〜ことは〜が|đúng là… nhưng…|V・イA thể thường／ナAな + ことは…が|読むことは読んだが、よく分からなかった。|Đúng là đã đọc nhưng không hiểu rõ.|〜には〜が~にはが~đúng là… nhưng…|!〜とは限らない~とはかぎらない~không nhất thiết
〜によって|tùy theo; bởi; bằng (phương tiện)|N + によって|原因によって、対応の方法が変わる。|Cách xử lý thay đổi tùy nguyên nhân.|〜に応じて~におうじて~tùy theo (một số ngữ cảnh)|!〜に対して~にたいして~đối với
〜に対して|đối với; trái với|N + に対して／thể thường + のに対して|お客様に対して、丁寧に説明する。|Giải thích lịch sự với khách hàng.|〜に向けて~にむけて~hướng tới (gần nghĩa trong một số ngữ cảnh)|!〜によって~によって~tùy theo, bởi
〜てほしい|muốn ai làm…|Ngườiに + Vて + ほしい|先生にもう一度説明してほしい。|Tôi muốn thầy cô giải thích thêm một lần.|〜てもらいたい~てもらいたい~muốn được ai làm cho|!〜たい~たい~bản thân muốn làm
〜ことだ|nên… (lời khuyên)|V từ điển／Vない + ことだ|困ったら、早めに相談することだ。|Nếu gặp khó khăn thì nên trao đổi sớm.|〜たほうがいい~たほうがいい~nên làm|!〜ことはない~ことはない~không cần làm
〜わけがない|không thể nào…|V・イA thể thường／ナAな／Nである + わけがない|あんなに真面目な人が嘘をつくわけがない。|Người nghiêm túc như vậy không thể nói dối.|〜はずがない~はずがない~không thể nào|!〜わけではない~わけではない~không hẳn là
〜代わりに|thay cho; thay vì; bù lại|Nの／V thể thường／ナAな + 代わりに|部長の代わりに、私が会議に出る。|Tôi dự họp thay trưởng phòng.|〜に代わって~にかわって~thay cho|!〜に加えて~にくわえて~thêm vào
〜ものか|đời nào…, nhất quyết không (khẩu ngữ: もんか)|V・イA thể thường／ナAな／Nな + ものか|途中であきらめるものか。|Nhất quyết không bỏ cuộc giữa chừng.|〜わけがない~わけがない~không thể nào (sắc thái khác)|!〜ものだ~ものだ~thường là, vốn là
〜そうもない|có vẻ không thể…, không có dấu hiệu…|gốc Vます + そうもない|今日は仕事が終わりそうもない。|Hôm nay có vẻ không thể xong việc.|〜そうにない~そうにない~có vẻ không thể|!〜そうだ~そうだ~có vẻ sẽ (dự đoán)
〜そうにない|có vẻ không…, khó có khả năng…|gốc Vます + そうにない|渋滞で、時間までに戻れそうにない。|Vì kẹt xe, có vẻ không thể về kịp giờ.|〜そうもない~そうもない~có vẻ không thể|!〜そうだ~そうだ~có vẻ sẽ
〜たばかり|vừa mới làm… (theo cảm nhận người nói)|Vた + ばかり|先月、ギターを買ったばかりです。|Tôi vừa mới mua đàn ghi-ta tháng trước.|〜たところ~たところ~vừa làm xong (ngay thời điểm đó)|!〜てから長い~てからながい~đã lâu kể từ khi
〜っぽい|có vẻ…, giống…, dễ có xu hướng…|N／gốc Vます／gốc イA + っぽい|この牛乳は水っぽい。|Sữa này loãng như nước.|〜みたい~みたい~giống như (cách nối khác)|!〜らしい~らしい~đúng chất, ra dáng (sắc thái khác)
〜さ|danh từ hóa tính chất: độ…, sự…|イA bỏ い／ナA bỏ な + さ|この部屋の静かさが好きです。|Tôi thích sự yên tĩnh của căn phòng này.|〜み~み~danh từ hóa một số tính từ (hạn chế hơn)|!〜い~い~đuôi tính từ (không phải danh từ)
〜としても|dù giả sử…, ngay cả nếu…|thể thường + としても (N／ナA dùng だ)|たとえ忙しいとしても、約束は守る。|Dù có bận cũng giữ lời hứa.|〜ても~ても~dù|!〜としたら~としたら~nếu giả sử
〜とは限らない|không nhất thiết…, không phải lúc nào cũng…|thể thường + とは限らない|高い物がいいとは限らない。|Đồ đắt không nhất thiết là tốt.|必ずしも〜ない~かならずしもない~không nhất thiết|!〜に違いない~にちがいない~chắc chắn là
〜に加えて|thêm vào…, ngoài… còn…|N + に加えて|テストに加えて、レビューも行う。|Ngoài kiểm thử còn tiến hành rà soát.|〜だけでなく~だけでなく~không chỉ… mà còn|!〜の代わりに~のかわりに~thay cho
〜恐れがある|có nguy cơ…, có thể xảy ra điều xấu|V từ điển／Nの + 恐れがある|大雨で、電車が遅れる恐れがある。|Có nguy cơ tàu bị trễ vì mưa lớn.|〜可能性がある~かのうせいがある~có khả năng (trung tính)|!〜心配はない~しんぱいはない~không lo ngại'''

ALIASES={'落として':'落とす','落ちて':'落ちる','割り当てた':'割り当てる','固まって':'固まる','延ばして':'延ばす','上がった':'上がる','繰り返して':'繰り返す','身につけた':'身につける','ふそく':'不足','なるべく早く':'なるべく'}

def relation(value):
    contrast=value.startswith('!');word,reading,meaning=value.lstrip('!').split('~')
    return dict(word=word,reading=reading,meaning=meaning,kind='contrast' if contrast else 'equivalent')

def build_learning(bank):
    lexicon={w['word']:dict(w) for w in bank['commonVocabulary']['words']}
    for line in ENRICH.splitlines():
        word,hv,translation,syn,ant=line.split('|')
        lexicon[word].update(hanViet=hv,translation=translation,synonyms=[relation(syn)],antonyms=[relation(ant)])
    for line in EXTRA.splitlines():
        word,reading,meaning,sentence,hv,translation,syn,ant=line.split('|')
        lexicon[word]=dict(word=word,reading=reading,meaning=meaning,sentence=sentence,hanViet=hv,translation=translation,synonyms=[relation(syn)],antonyms=[relation(ant)])
    # Base nouns reuse the corresponding する entry, retaining a dictionary form for study.
    for word,entry in list(lexicon.items()):
        if word.endswith('する'):
            base=word[:-2];lexicon.setdefault(base,{**entry,'word':base,'reading':entry['reading'][:-2]})
    tok=Tokenizer();unknown=set()
    overrides={'進捗':'しんちょく','進捗率':'しんちょくりつ','買掛金':'かいかけきん','依存':'いぞん','朝会':'ちょうかい'}
    def hira(text):return ''.join(chr(ord(c)-0x60) if 'ァ'<=c<='ヶ' else c for c in text)
    def token_ruby(text):
        parts=[]
        for token in tok.tokenize(text):
            surface=token.surface
            if re.search(r'[一-龯々]',surface):
                reading=overrides.get(surface,lexicon.get(surface,{}).get('reading',hira(token.reading)))
                if reading=='*':unknown.add(surface);reading=''
                end=0
                while end<min(len(surface),len(reading)) and surface[-end-1]==reading[-end-1] and not re.search(r'[一-龯々]',surface[-end-1]):end+=1
                if end:parts.extend([dict(text=surface[:-end],reading=reading[:-end]),dict(text=surface[-end:])])
                else:parts.append(dict(text=surface,reading=reading))
            else:parts.append(dict(text=surface))
        return parts
    # Context-sensitive compounds that the tokenizer otherwise splits incorrectly.
    fixed={'九時':'くじ','仕入先':'しいれさき','今日中':'きょうじゅう'}
    fixed_re=re.compile('|'.join(map(re.escape,fixed)))
    def ruby(text):
        parts=[];cursor=0
        for match in fixed_re.finditer(text):
            parts.extend(token_ruby(text[cursor:match.start()]))
            parts.append(dict(text=match.group(),reading=fixed[match.group()]))
            cursor=match.end()
        parts.extend(token_ruby(text[cursor:]));return parts
    for entry in lexicon.values():
        entry['exampleRuby']=ruby(entry['sentence'])
        entry['wordRuby']=ruby(entry['word'])
    patterns={}
    for line in GRAMMAR.splitlines():
        pattern,meaning,form,sentence,translation,syn,ant=line.split('|')
        patterns[pattern]=dict(word=pattern,meaning=meaning,form=form,sentence=sentence,translation=translation,exampleRuby=ruby(sentence),synonyms=[relation(syn)],antonyms=[relation(ant)])
    grammar_kanji={'〜一方で':('いっぽうで','nhất phương'),'〜に対して':('にたいして','đối'),'〜代わりに':('かわりに','đại'),'〜とは限らない':('とはかぎらない','hạn'),'〜に加えて':('にくわえて','gia'),'〜恐れがある':('おそれがある','khủng')}
    for pattern,(reading,hv) in grammar_kanji.items():
        patterns[pattern].update(reading=reading,hanViet=hv,wordRuby=ruby(pattern))
    def lookup(q):
        if q.get('word'):return q['word']
        key=q['options'][q['answer']] if q['type'] in ('kanji','context') else q['target']
        key=ALIASES.get(key,key)
        if key not in lexicon:raise ValueError(f"Missing study word: {key} in {q['id']}")
        return key
    for unit in bank['units']:
        for q in unit['vocabulary']:q['studyKey']=lookup(q)
        for q in unit['grammar']:
            if q['pattern'] not in patterns:raise ValueError(q['pattern'])
            q['studyPattern']=q['pattern']
    for q in bank['commonVocabulary']['questions']:q['studyKey']=lookup(q)
    if unknown:raise ValueError(f'Unknown example readings: {sorted(unknown)}')
    bank['learning']=dict(vocabulary=lexicon,grammar=patterns,note='Từ mở rộng để luyện JLPT; không phải danh sách hay thống kê tần suất chính thức. Từ đối chiếu được ghi rõ và không mặc định là trái nghĩa.',source='https://www.jlpt.jp/e/faq/')
    return bank

if __name__=='__main__':
    path=Path(__file__).parent/'dist/questions.json'
    bank=build_learning(json.loads(path.read_text(encoding='utf-8')))
    path.write_text(json.dumps(bank,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f"Added study cards: {len(bank['learning']['vocabulary'])} vocabulary entries and {len(bank['learning']['grammar'])} patterns.")
