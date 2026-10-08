"""Danh sách từ vựng chung người dùng cung cấp; 対応する được gộp một lần."""
import random, re
from exam_update import INSTRUCTIONS

# word | reading | Vietnamese meaning | Japanese paraphrase | example sentence
WORDS = {
'noun': '''貿易|ぼうえき|ngoại thương, thương mại quốc tế|国どうしで商品を売買すること|日本は多くの国と貿易をしている。
輸出|ゆしゅつ|xuất khẩu|商品を外国へ売って送り出すこと|この会社は機械の輸出を行っている。
輸入|ゆにゅう|nhập khẩu|外国の商品を国内へ買い入れること|海外から食品を輸入する。
機能|きのう|chức năng|機械やシステムが果たす働き|アプリに新しい機能を追加する。
単体テスト|たんたいテスト|kiểm thử từng thành phần riêng lẻ|一つの部品や機能を個別に確かめるテスト|実装した関数の単体テストを行う。
結合テスト|けつごうテスト|kiểm thử tích hợp|複数の部品を組み合わせて動きを確かめるテスト|モジュール間の連携を結合テストで確認する。
試験項目|しけんこうもく|hạng mục kiểm thử|テストで確認する個々の内容|試験項目を一覧にまとめる。
進捗|しんちょく|tiến độ|作業がどこまで進んだかという状況|朝会で開発の進捗を報告する。
注意点|ちゅういてん|điểm cần lưu ý|気をつける必要がある点|作業を始める前に注意点を確認する。
統一|とういつ|thống nhất|ばらばらのものを同じ基準にそろえること|チーム内で書式の統一を図る。
予定|よてい|kế hoạch, dự định|これから行うと決めていること|明日の予定を確認する。
程度|ていど|mức độ|物事の大きさや強さの度合い|エラーの程度によって対応を変える。
朝会|ちょうかい|buổi họp đầu giờ sáng|朝に開く短い会議|毎朝九時に朝会を行う。
課題|かだい|nhiệm vụ hoặc vấn đề cần giải quyết|取り組んで解決すべき問題|現在の課題をチームで話し合う。
開発|かいはつ|phát triển sản phẩm, phần mềm|新しい製品やシステムを作り出すこと|新しいアプリの開発を進める。
担当|たんとう|việc phụ trách, người phụ trách|仕事を受け持つことやその人|この機能の担当は田中さんです。
数字|すうじ|chữ số, con số|数を表す文字|報告書の数字を確認する。
件数|けんすう|số vụ, số trường hợp|事柄や案件の数|一日の問い合わせ件数を数える。
消化|しょうか|xử lý xong công việc; tiêu hóa|予定した仕事などを次々にこなすこと|予定していた作業をすべて消化した。
トラブル|トラブル|sự cố, rắc rối|問題やもめごと|システムにトラブルが発生した。
解決策|かいけつさく|phương án giải quyết|問題を解決するための方法|チームで解決策を考える。
遅れ|おくれ|sự chậm, sự trễ|予定より遅くなること|作業の遅れを報告する。
遅延|ちえん|sự trì hoãn, chậm trễ|処理や進行が予定の時刻より遅れること|通信の遅延を調べる。
事実|じじつ|sự thật|実際に起こったこと|推測ではなく事実を確認する。
進捗率|しんちょくりつ|tỷ lệ hoàn thành công việc|全体に対して完了した作業の割合|現在の進捗率は八十パーセントです。
工程|こうてい|công đoạn, bước trong quy trình|製造や開発で順番に行う作業の区切り|次の工程へ進む。
詳細|しょうさい|chi tiết|細かく詳しい内容|仕様の詳細を確認する。
影響|えいきょう|ảnh hưởng|ある物事がほかの物事に及ぼす作用|変更の影響を調査する。
原因|げんいん|nguyên nhân|物事を引き起こしたもと|エラーの原因を調べる。
段階|だんかい|giai đoạn, cấp độ|物事が進む途中の一つの区切り|開発はテストの段階に入った。
不足|ふそく|sự thiếu hụt|必要な量に足りないこと|人手の不足を解消したい。
主流|しゅりゅう|xu hướng chính, cách làm phổ biến|中心となって広く使われている傾向|今はこの方法が主流だ。
難易度|なんいど|mức độ khó dễ|難しさや易しさの度合い|課題の難易度を確認する。
規模|きぼ|quy mô|組織や事業などの大きさ|プロジェクトの規模が大きい。
状態|じょうたい|trạng thái|ある時点での物事のありさま|機器の状態を確認する。
作業|さぎょう|công việc, thao tác|目的のために行う具体的な仕事|今日の作業を始める。
余裕|よゆう|thời gian, năng lực hoặc phần dư|時間や能力などにゆとりがあること|締切までまだ余裕がある。
最善|さいぜん|tốt nhất trong các khả năng|考えられる中でいちばんよいこと|最善の方法を選ぶ。
締め切り|しめきり|hạn chót|提出や申し込みを終える期限|レポートの締め切りは金曜日だ。
直前|ちょくぜん|ngay trước thời điểm nào đó|あることが起こるすぐ前|会議の直前に資料を確認した。
遅刻|ちこく|việc đến muộn|決められた時刻より遅く到着すること|寝坊して会社に遅刻した。
部署|ぶしょ|bộ phận, phòng ban|組織の中で仕事を分けて受け持つ部門|来月から別の部署で働く。
資料|しりょう|tài liệu|判断や説明のために使う情報や文書|会議の資料を準備する。
導入|どうにゅう|việc đưa vào sử dụng|新しい制度や道具を取り入れること|新しいツールの導入を検討する。
状況|じょうきょう|tình hình, hoàn cảnh|周囲も含めた物事の成り行きや様子|現在の状況を報告する。
経験|けいけん|kinh nghiệm|実際に行ったり体験したりして得たもの|彼は開発の経験が豊富だ。
可能性|かのうせい|khả năng có thể xảy ra|あることが起こりうる見込み|予定が変わる可能性がある。''',
'verb': '''注文する|ちゅうもんする|đặt mua hàng hoặc gọi món|商品や料理を頼んで買おうとする|店で必要な商品を注文する。
発注する|はっちゅうする|đặt hàng với nhà cung cấp|取引先に商品や仕事の注文を出す|仕入先に部品を発注する。
管理する|かんりする|quản lý|物事を整えて適切に保つ|リーダーが進捗を管理する。
準備する|じゅんびする|chuẩn bị|必要なものを前もってそろえる|会議の資料を準備する。
実施する|じっしする|thực hiện, tiến hành|計画したことを実際に行う|明日、単体テストを実施する。
進める|すすめる|tiến hành, đẩy tiến độ|物事を先へ運ぶ|計画に沿って開発を進める。
共有する|きょうゆうする|chia sẻ, cùng có thông tin|情報などを複数の人が共通に持つ|注意点をチームで共有する。
完了する|かんりょうする|hoàn tất|必要な作業をすべて終える|今日中に作業を完了する。
残業する|ざんぎょうする|làm thêm giờ|決められた勤務時間を過ぎて働く|納期が近いので今日は残業する。
相談する|そうだんする|trao đổi để xin ý kiến|問題について相手と話して意見を求める|困ったら先輩に相談する。
隠す|かくす|giấu, che giấu|人に見えないようにする|ミスを隠すのはよくない。
対応する|たいおうする|ứng phó, xử lý phù hợp|状況や相手に応じて行動する|お客様の問い合わせに対応する。
終了する|しゅうりょうする|kết thúc|続いていたことが終わる|五時に会議が終了する。
提出する|ていしゅつする|nộp, trình tài liệu|書類などを決められた相手に出す|レポートを先生に提出する。
報告する|ほうこくする|báo cáo|結果や状況を相手に知らせる|作業の遅れをリーダーに報告する。
依存する|いぞんする|phụ thuộc, dựa vào|ほかのものに頼って成り立つ|この機能は外部システムに依存する。
調整する|ちょうせいする|điều chỉnh|条件に合うように整える|会議の日程を調整する。
回避する|かいひする|tránh, né|危険や問題を避ける|事前の確認でトラブルを回避する。
調査する|ちょうさする|điều tra, khảo sát|事実を明らかにするために調べる|エラーの原因を調査する。
取り戻す|とりもどす|lấy lại, khôi phục|失ったものを再び手に入れる|バックアップからデータを取り戻す。
限る|かぎる|giới hạn|範囲をそれだけに制限する|参加者を十人に限る。
進行する|しんこうする|diễn tiến, tiến hành|物事が先へ進んでいく|会議は予定どおり進行する。
増員する|ぞういんする|tăng nhân sự|働く人の数を増やす|作業が増えたのでスタッフを増員する。
統計する|とうけいする|thống kê|数値を集めて整理し全体の傾向を示す|毎月の件数を統計する。
出荷する|しゅっかする|xuất hàng, gửi hàng đi|商品を倉庫や工場から送り出す|注文された商品を出荷する。
編集する|へんしゅうする|biên tập, chỉnh sửa nội dung|文章や動画を整理して作り直す|撮影した動画を編集する。
返品する|へんぴんする|trả lại hàng đã mua|買った商品を店に返す|壊れていた商品を返品する。
慌てる|あわてる|luống cuống, hốt hoảng|急なことに落ち着きを失う|エラーが出ても慌てる必要はない。
提案する|ていあんする|đề xuất|考えた案を相手に示す|新しい方法を提案する。
連携する|れんけいする|phối hợp, liên kết|互いに協力して働く|二つの部署が連携する。
支援する|しえんする|hỗ trợ|活動や仕事を助ける|会社は新人の学習を支援する。
修正する|しゅうせいする|sửa lại lỗi hoặc nội dung|間違っている部分を直す|コードの間違いを修正する。
検討する|けんとうする|xem xét, cân nhắc kỹ|よく調べて考える|新しいツールの導入を検討する。
頼む|たのむ|nhờ, yêu cầu|相手にお願いする|先輩に確認を頼む。
追加する|ついかする|thêm vào|あとからさらに足す|試験項目を追加する。
加える|くわえる|bổ sung, thêm|すでにあるものに別のものを足す|資料に説明を加える。''',
'adjective': '''個性的|こせいてき|có cá tính, có nét riêng|その人や物らしい特徴がある様子|彼のデザインは個性的だ。
具体的|ぐたいてき|cụ thể|内容がはっきり示されている様子|具体的な解決策を考える。
順調|じゅんちょう|thuận lợi|問題なくうまく進んでいる様子|作業は順調だ。
技術的|ぎじゅつてき|về mặt kỹ thuật|技術に関係する様子|技術的な問題を調査する。
重要|じゅうよう|quan trọng|大切で欠かせない様子|これは重要な注意点だ。
正確|せいかく|chính xác|間違いやずれがない様子|正確な数字を報告する。
複雑|ふくざつ|phức tạp|多くの要素が入り組んでいる様子|この機能は複雑だ。
重大|じゅうだい|nghiêm trọng, hệ trọng|影響が大きく深刻な様子|重大なバグを発見した。
普通|ふつう|bình thường|特別ではなく一般的な様子|普通の使い方なら問題はない。
簡単|かんたん|đơn giản, dễ|難しくなく手軽な様子|これは簡単な作業だ。
適当|てきとう|phù hợp trong ngữ cảnh này|条件や目的に合っている様子|目的に適当な方法を選ぶ。''',
'adverb': '''正直に|しょうじきに|một cách thành thật|うそをつかずに|問題があれば正直に報告してください。
早めに|はやめに|sớm hơn, sớm một chút|予定や通常より少し早く|資料を早めに提出する。
速やかに|すみやかに|nhanh chóng, kịp thời|時間をかけず手早く|トラブルには速やかに対応する。
すぐに|すぐに|ngay lập tức|待たずにただちに|分からないことはすぐに相談する。
ゆっくり|ゆっくり|chậm rãi, thong thả|急がず時間をかけて|説明をゆっくり読んでください。
たまに|たまに|thỉnh thoảng, không thường xuyên|まれに、ときおり|彼はたまに残業する。
時々|ときどき|đôi khi, từng lúc|ときおり、何度か|このエラーは時々発生する。
しっかり|しっかり|kỹ càng, chắc chắn|十分に、きちんと|要件をしっかり確認する。
なるべく|なるべく|cố gắng trong khả năng, càng ... càng tốt|できるだけ|なるべく早く報告してください。
やっと|やっと|cuối cùng cũng, sau nhiều nỗ lực|苦労してようやく|長いテストがやっと終わった。
たぶん|たぶん|có lẽ, chắc là|おそらく|たぶん明日には完了するでしょう。
わざと|わざと|cố ý|意図的に、故意に|確認のためにわざとエラーを発生させた。''',
'katakana': '''タイミング|タイミング|thời điểm thích hợp|物事を行う時機|報告するタイミングを考える。
コーディング|コーディング|việc viết mã chương trình|プログラムのコードを書くこと|設計の後でコーディングを始める。
ロジック|ロジック|logic, cách xử lý có hệ thống|処理や考え方の筋道|計算のロジックを確認する。
リーダー|リーダー|người lãnh đạo, trưởng nhóm|集団をまとめて導く人|リーダーが作業を割り当てる。
メンバー|メンバー|thành viên|集団を構成する一人一人|チームのメンバーに相談する。
プログラム|プログラム|chương trình máy tính|コンピューターに行わせる命令の集まり|新しいプログラムを実行する。
チーム|チーム|nhóm cùng làm việc|同じ目的のために協力する集団|チームで情報を共有する。
エラー|エラー|lỗi trong xử lý hoặc vận hành|処理中に起きる誤り|入力のエラーを確認する。
クレーム|クレーム|phản ánh, khiếu nại của khách hàng|商品やサービスへの苦情|お客様のクレームに対応する。
バグ|バグ|lỗi trong chương trình|プログラムに含まれる不具合|テストでバグを発見する。
ツール|ツール|công cụ|作業を助ける道具|便利なツールを導入する。
モジュール|モジュール|mô-đun, bộ phận chức năng|独立した機能を持つ構成部分|二つのモジュールを結合する。'''
}

# Ngữ cảnh với các phương án cùng loại nhưng khác nghĩa.
CONTEXTS = '''海外の商品を国内へ買い入れることを（　）という。|輸入|輸出,出荷する,返品する|輸入 là nhập khẩu, đưa hàng nước ngoài vào trong nước.
国内の商品を外国へ売ることを（　）という。|輸出|輸入,部署,資料|輸出 là xuất khẩu.
関数を一つずつ独立して確認するため、（　）を行った。|単体テスト|結合テスト,貿易,朝会|単体テスト kiểm thử riêng từng thành phần.
複数のモジュールを接続し、連携が正しいか（　）で確認した。|結合テスト|単体テスト,資料,締め切り|結合テスト kiểm thử các thành phần hoạt động cùng nhau.
全体のうち完了した作業の割合を、（　）で示す。|進捗率|件数,原因,部署|進捗率 là tỷ lệ hoàn thành so với tổng công việc.
問い合わせが何件あったか、その（　）を数える。|件数|難易度,主流,タイミング|件数 là số vụ hoặc số trường hợp.
百という数を表す「100」は、三つの（　）で書かれている。|数字|部署,工程,解決策|数字 là ký hiệu chữ số.
レポートを提出できる最後の日が（　）だ。|締め切り|経験,主流,機能|締め切り là hạn chót.
会社の営業部や開発部は、異なる（　）である。|部署|数字,進捗率,原因|部署 là phòng hoặc bộ phận trong tổ chức.
商品の注文を取引先へ出すことを（　）という。|発注する|返品する,隠す,残業する|発注する: đặt hàng với nhà cung cấp.
買った商品が壊れていたので、店に（　）ことにした。|返品する|輸出,導入,依存する|返品する: trả lại hàng đã mua.
決められた勤務時間の後も働くことを（　）という。|残業する|回避する,輸入,注文する|残業する: làm thêm giờ.
情報を複数の人が共通に持つことを（　）という。|共有する|隠す,返品する,慌てる|共有する: chia sẻ, cùng có thông tin.
間違っているコードの部分を正しく（　）。|修正する|輸入,増員する,返品する|修正する: sửa lại lỗi.
作業が増えたので、スタッフの人数を（　）ことにした。|増員する|返品する,輸出,隠す|増員する: tăng nhân sự.
発生したミスを隠さず、（　）報告してください。|正直に|わざと,たまに,たぶん|正直に: thành thật, không giấu hoặc nói dối.
急がなくていいので、（　）説明してください。|ゆっくり|速やかに,すぐに,やっと|ゆっくり: chậm rãi; 急がなくていい đặt ngữ cảnh không cần vội.
テストのために、偶然ではなく（　）エラーを発生させた。|わざと|たぶん,やっと,たまに|わざと: cố ý; đối lập với ngẫu nhiên.
長い間苦労して、（　）問題を解決できた。|やっと|わざと,時々,たぶん|やっと: cuối cùng đạt được sau nhiều khó khăn.
アプリを動かす命令の集まりが（　）だ。|プログラム|クレーム,リーダー,貿易|プログラム: tập hợp chỉ thị để máy tính thực hiện.
お客様から商品についての苦情、つまり（　）が届いた。|クレーム|モジュール,コーディング,タイミング|クレーム: phản ánh hoặc khiếu nại.
プログラムのコードを書く作業を（　）という。|コーディング|タイミング,メンバー,クレーム|コーディング: viết mã chương trình.
チームをまとめて導く人が（　）だ。|リーダー|モジュール,プログラム,ツール|リーダー: người lãnh đạo nhóm.
間違いやずれがなく、（　）な数字を報告する。|正確|複雑,重大,普通|正確: chính xác.
多くの要素が入り組んで、仕組みが（　）だ。|複雑|簡単,順調,正確|複雑: phức tạp, nhiều yếu tố đan xen.'''

USAGES = '''進捗|毎朝、作業の進捗を報告する。|作業を進捗に報告する。^作業は進捗な終わる。^進捗が作業を報告なった。|作業の進捗: tiến độ công việc.
依存する|この機能は外部システムに依存している。|この機能を外部システムが依存にした。^この機能は依存なシステムだ。^外部システムを依存に報告した。|Nに依存する: phụ thuộc vào N. いぞん và いそん đều được dùng.
増員する|人手が足りないので、スタッフを増員する。|パソコンの台数を増員する。^アプリの機能を増員する。^会議室の数を増員する。|増員 dùng cho tăng số người, không dùng cho thiết bị hoặc chức năng.
提出する|完成した資料をリーダーに提出する。|完成した資料がリーダーを提出する。^完成した資料を提出な見せる。^資料は提出に完成した。|Tài liệu を + người に提出する: nộp tài liệu.
複雑|この機能は複雑なので、確認に時間がかかる。|この機能は複雑を確認する。^この機能は複雑する確認だ。^この機能を複雑に時間する。|複雑 là tính từ な: 複雑な機能, 機能は複雑だ.
しっかり|作業前に要件をしっかり確認する。|要件はしっかりな確認だ。^要件をしっかりに確認する。^要件がしっかりを作業する。|しっかり làm trạng từ trực tiếp trước động từ.
発注する|仕入先に必要な部品を発注する。|仕入先が部品を発注な準備する。^必要な部品を発注に買う。^部品は発注な仕入先だ。|Người hoặc công ty に + hàng hóa を発注する.
締め切り|資料の締め切りは金曜日です。|金曜日を締め切りな提出した。^資料が締め切りを提出する。^金曜日に締め切りを資料した。|締め切り là danh từ chỉ hạn chót.
追加する|必要な試験項目をリストに追加する。|必要な試験項目がリストを追加する。^リストは追加な項目だ。^試験項目を追加に書いた。|Thứ を + nơi に追加する: thêm một mục vào danh sách.
対応する|担当者がお客様の問い合わせに対応する。|問い合わせが担当者を対応する。^担当者は対応な問い合わせをした。^問い合わせを対応に聞いた。|Nに対応する: xử lý đối với câu hỏi, yêu cầu, tình huống.
連携する|開発チームとテストチームが連携して作業する。|開発チームを連携な作業する。^テストチームが連携に協力した。^連携をチームに集める。|Nと連携する: phối hợp cùng nhóm hoặc tổ chức khác.
速やかに|問題が起きたら、速やかに対応する。|速やかを対応する。^速やかにの問題を起こす。^速やかにが問題をした。|速やかに: nhanh chóng, kịp thời; dùng như trạng từ.'''

def build_common():
    rng=random.Random(118)
    entries=[]
    for category, lines in WORDS.items():
        for line in lines.splitlines():
            word,reading,meaning,paraphrase,sentence=line.split('|')
            entries.append(dict(word=word,reading=reading,meaning=meaning,paraphrase=paraphrase,sentence=sentence,category=category))
    assert len(entries)==118 and len({e['word'] for e in entries})==118
    questions=[]
    def add(typ, target, correct, wrong, exp, **extra):
        options=[correct]+wrong
        assert len(options)==len(set(options))==4, (target,options)
        rng.shuffle(options)
        questions.append(dict(id=f'common-{len(questions)+1:03d}',type=typ,prompt=INSTRUCTIONS[typ],target=target,
                              options=options,answer=options.index(correct),explanation=exp,
                              group={'reading':1,'kanji':2,'context':3,'synonym':4,'usage':5}[typ],**extra))
    # Danh sách có hai cách đọc được chấp nhận. Không dùng 依存する cho dạng cách đọc.
    ambiguous={'依存する'}
    equivalent={'追加する':{'加える'},'加える':{'追加する'},'遅れ':{'遅延'},'遅延':{'遅れ'},'たまに':{'時々'},'時々':{'たまに'}}
    for e in entries:
        word=e['word']; candidates=[x for x in entries if x['word']!=word and x['word'] not in equivalent.get(word,set()) and x['category']==e['category']]
        if re.search(r'[一-龯]',word) and word not in ambiguous:
            # Nhiễu chỉ thay một âm kana để kiểm tra trường âm, âm ngắt và âm Hán.
            kana=e['reading']; forms=[]
            replacements={'う':'お','っ':'つ','し':'じ','じ':'し','か':'が','が':'か','き':'ぎ','く':'ぐ','た':'だ','ち':'じ','て':'で','は':'ば','け':'げ','と':'ど','ん':'う','ょ':'よ','ゅ':'ゆ'}
            for i,c in enumerate(kana):
                if c in replacements: forms.append(kana[:i]+replacements[c]+kana[i+1:])
            forms=list(dict.fromkeys(f for f in forms if f!=kana))
            # Bổ sung cách đọc gần nghĩa không đúng cho chính từ này nếu thiếu biến thể âm.
            while len(forms)<3:
                alternative=rng.choice(candidates)['reading']
                if alternative!=kana and alternative not in forms: forms.append(alternative)
            add('reading',word,kana,forms[:3],f"{word} đọc là {kana}: {e['meaning']}.",sentence=e['sentence'],word=word)
            wrong=[x['word'] for x in rng.sample(candidates,3)]
            add('kanji',kana,word,wrong,f"{kana} viết là {word}: {e['meaning']}.",sentence=e['sentence'].replace(word,kana),word=word)
        wrong=[x['paraphrase'] for x in rng.sample(candidates,3)]
        note=' 適当 còn có nghĩa làm qua loa trong ngữ cảnh khác; câu này dùng nghĩa phù hợp.' if word=='適当' else ''
        note+=' いぞんする và いそんする đều được dùng.' if word=='依存する' else ''
        add('synonym',word,e['paraphrase'],wrong,f"{word} ({e['reading']}): {e['meaning']}."+note,sentence=e['sentence'],word=word)
    for line in CONTEXTS.splitlines():
        sentence,correct,wrong,exp=line.split('|')
        add('context',sentence,correct,wrong.split(','),exp,word=correct)
    for line in USAGES.splitlines():
        word,correct,wrong,exp=line.split('|')
        add('usage',word,correct,wrong.split('^'),exp,word=word)
    return dict(id='common',title='Từ vựng chung',words=entries,questions=questions,sessionSize=40,
                sourceNote='Toàn bộ bảng từ vựng chung người dùng cung cấp. 対応する xuất hiện hai lần được gộp thành một từ. Ngân hàng gồm các dạng đọc, chữ Hán, điền từ, gần nghĩa và cách dùng.')
