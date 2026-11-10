# Lovers Kernel BakaSU

**機械学習によるチューニングと連携する、Pixel向けカスタムカーネル。**

| 対象シリーズ | Pixel 11 / Pixel 11 Pro / Pixel 11 Pro XL |
|---|---|

[English](README.md) | [日本語](README_ja.md)

Lovers Kernel BakaSUは、**Pixel 11シリーズ**を対象に、CPUスケジューリング・メモリ管理・ストレージ・ネットワークの変更をまとめたカスタムカーネルです。**BakaSU**をカーネルへ組み込み、**Lovers Kernel Tuner**による学習・設定管理と連携します。

## 主な機能

| 分類 | 内容 |
|---|---|
| CPUスケジューラー | Android EEVDF上のBORE、CASSによるCPU配置 |
| IRQ負荷分散 | CPUの処理能力を考慮するSBalanceと稼働統計 |
| CPU周波数・アイドル | Schedutil調整、TEOの予測処理修正、CPU latency QoS設定 |
| メモリ管理 | DAMON/DAMOSによる適応型回収、mTHP、MGLRU調整 |
| ZRAM | 純正Google ZRAMとEH圧縮を維持 |
| ストレージ | ADIOS I/Oスケジューラー、TMPFS対応、F2FS／EROFSの不具合修正 |
| ネットワーク | BBRv3、CAKE、fq_codel対応 |
| 電力関連 | RCU_LAZY、省電力向けworkqueue設定 |
| root・SUSFS・保護機能 | BakaSU、SUSFS、UID isolation対応NoMountの組み込み、Baseband Guard（BBG） |
| ビルド | CFIを維持したNoLTO構成 |

実際に働く機能は、端末・使用中のCPUFreqガバナー・実行時設定によって異なります。Schedutilの設定はschedutil使用時が対象です。CASSは既定でAndroid vendor hookの有効なCPU選択を優先し、SBalanceは初期状態でOFF、idle QoSの要求は解除状態です。CAKE対応だけで通信インターフェースのキューを自動的に切り替えるわけではありません。

## 連携ツール

### Lovers Kernel Tuner

**Lovers Kernel Tuner**は、対応するカーネルインターフェースを利用した学習・統計表示・設定管理に対応しています。

インストール後にアプリを開き、root権限を許可してください。利用できる制御は、稼働中のカーネル・ガバナー・端末が公開するインターフェースによって異なります。純正Google ZRAMを維持するため、APatch版にある汎用ZRAMの再圧縮制御を、このカーネルで有効化するものではありません。

スケジューリングや調整機構はカーネルが提供し、アプリは対応する設定を管理します。このリリースでの性能・FPS・電池持ちの改善率は未測定です。

## 使用方法

| 配布物 | 使用方法 |
|---|---|
| カーネル`boot,img` | fastbootモードでflashまたはbootで起動してください |
| BakaSU Manager | 対応するマネージャーをインストールしてroot権限を管理 |
| Lovers Kernel Tuner APK | Androidアプリとしてインストールし、初回起動時にrootを許可 |

現在の変更はImageのみの差し替えを想定しており、交換用koの導入は不要です。NoMountのルール設定には、対応するv2.2.0／protocol22のメタモジュールを使用します。

## クレジット・ライセンス

Linux kernel、Android Common Kernel、Google Pixel kernel、BakaSU、KernelSU、SUSFS、NoMount、Baseband Guard、BBR、BORE、ADIOS、Sultan kernelなど、本プロジェクトの基盤となった開発者・貢献者の皆様に感謝します。Sultan関連の変更はAndroid 6.12向けに調整した移植です。各ソースの著作権表示・ライセンスを維持しています。
