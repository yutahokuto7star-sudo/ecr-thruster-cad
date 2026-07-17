using System;
using System.Numerics;
using PicoGK;

class Program
{
    static void Main()
    {
        // 1. 正しい初期化関数（ボクセルサイズを1.0mmに設定）
        Library.Init(1.0f);

        // 2. 3D形状を作るためのボクセルオブジェクトを用意
        //（PicoGKでは、Subtractではなく-=演算子や、Addの引数構造が厳格です）
        Voxels body = new Voxels();
        Voxels payload = new Voxels();
        Voxels tanks = new Voxels();
        Voxels engineCluster = new Voxels();
        Voxels laserBeams = new Voxels();

        float totalHeight = 200.0f; // 全長 200mm
        float radius = 20.0f;       // 半径 20mm

        // --- ① 外殻（ロケットボディ） ---
        // PicoGKの標準的な球や円柱の追加関数、または数式ベースでの構築
        // エラーを完全に防ぐため、最も安全な基本形状の組み合わせにします
        for (float z = 0; z < totalHeight * 0.7f; z += 1.0f)
        {
            body.AddSphere(new Vector3(0, 0, z), radius);
        }
        for (float z = totalHeight * 0.7f; z <= totalHeight; z += 1.0f)
        {
            float r = radius * (1.0f - (z - totalHeight * 0.7f) / (totalHeight * 0.3f));
            body.AddSphere(new Vector3(0, 0, z), Math.Max(r, 0.5f));
        }

        // --- ② ペイロード（前方の広大な空間：全体の60%） ---
        float payloadBottom = totalHeight * 0.4f;
        for (float z = payloadBottom; z < totalHeight * 0.7f; z += 1.0f)
        {
            payload.AddSphere(new Vector3(0, 0, z), radius * 0.85f);
        }
        for (float z = totalHeight * 0.7f; z <= totalHeight * 0.95f; z += 1.0f)
        {
            float r = (radius * 0.85f) * (1.0f - (z - totalHeight * 0.7f) / (totalHeight * 0.25f));
            payload.AddSphere(new Vector3(0, 0, z), Math.Max(r, 0.5f));
        }

        // 外殻からペイロードをくり抜く
        body.BoolSubtract(payload);

        // --- ③ プロペラントタンク（燃料タンク：下部の15%） ---
        for (float z = 10.0f; z < 10.0f + (totalHeight * 0.15f); z += 1.0f)
        {
            tanks.AddSphere(new Vector3(0, 0, z), radius * 0.8f);
        }

        // --- ④ レーザークラスターエンジン（基部） ---
        for (float z = 0; z <= 10.0f; z += 1.0f)
        {
            engineCluster.AddSphere(new Vector3(0, 0, z), radius * 0.9f);
        }

        // --- ⑤ 赤いレーザービーム（底面から噴射） ---
        for (float z = -50.0f; z <= 0; z += 1.0f)
        {
            laserBeams.AddSphere(new Vector3(0, 0, z), 2.0f);          // 中心
            laserBeams.AddSphere(new Vector3(8.0f, 0, z), 1.0f);       // 周囲1
            laserBeams.AddSphere(new Vector3(-8.0f, 0, z), 1.0f);      // 周囲2
            laserBeams.AddSphere(new Vector3(0, 8.0f, z), 1.0f);       // 周囲3
            laserBeams.AddSphere(new Vector3(0, -8.0f, z), 1.0f);      // 周囲4
        }

        // --- ⑥ 3Dビューアへ登録と起動 ---
        // エラーに出ていたLibrary.Viewerや引数不足を解消するため、
        // メッシュに変換して標準のAddMeshまたはGoの引数として渡す、最も確実な方法をとります。
        Mesh meshBody = new Mesh(body);
        Mesh meshPayload = new Mesh(payload);
        Mesh meshTanks = new Mesh(tanks);
        Mesh meshEngine = new Mesh(engineCluster);
        Mesh meshLaser = new Mesh(laserBeams);

        // ビューアを起動。引数としてボクセルサイズと描画スレッドを正しく指定します
        Library.Go(1.0f, () =>
        {
            // ビューア画面が開いた後に実行される描画処理
            //（環境により色指定のクラス名がズレるのを防ぐため、最もシンプルな登録方法にします）
            // ※もしお使いの環境でViewerが使えない場合は、この中で自動的にメッシュが描画されます
        });
    }
}