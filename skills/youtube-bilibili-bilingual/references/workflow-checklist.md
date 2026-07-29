# Checklist

## Inputs
- [ ] YouTube URL
- [ ] Optional B 站标题（无「中上英下」）
- [ ] 原频道名
- [ ] 是否上传 / 是否发时间戳评论

## Process
- [ ] yt-dlp 最高画质 + 封面 + info.json
- [ ] Whisper large-v3（防幻觉参数）
- [ ] ASS 中上大字 / 英下小字
- [ ] FFmpeg 硬字幕成片
- [ ] 简介转载声明 + 中英要点/排名
- [ ] cookie 存在后再 biliup `copyright=2`
- [ ] 时间戳评论（中英名 + 00:00:00）

## Deliverables
- [ ] final_bilibili_video.mp4
- [ ] bilingual_subs.srt / .ass
- [ ] bilibili_description.txt
- [ ] BV 链接（若已上传）
