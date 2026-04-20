"""
interceptor.py — Passive network interception layer.

Subscribes to page.on('response') events and extracts Instagram
post data from background GraphQL / JSON responses on the fly.
Uses defensive programming (.get()) to handle Instagram's
ever-changing response shapes.
"""
import json
import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any, Optional

log = logging.getLogger(__name__)

AI_KEYWORDS = [k.strip().lower() for k in "ai, a.i., artificial intelligence, ии, искусственный интеллект, нейросеть, нейросети, нейронка, нейронки, llm, large language model, большая языковая модель, genai, generative ai, генеративный ии, agi, artificial general intelligence, asi, artificial superintelligence, machine learning, ml, deep learning, глубокое обучение, машинное обучение, neural network, neural networks, natural language processing, nlp, computer vision, transformer, transformers, foundation model, frontier model, multimodal, multimodal ai, text-to-image, text-to-video, text-to-speech, text-to-3d, image-to-video, speech-to-text, ai model, ai models, language model, language models, small language model, slm, open source ai, open-source ai, ai safety, ai alignment, ai ethics, ai regulation, superintelligence, inference, fine-tuning, fine-tune, finetuning, rlhf, reinforcement learning, supervised learning, unsupervised learning, few-shot, zero-shot, chain of thought, cot, rag, retrieval augmented generation, vector database, vector db, embeddings, embedding model, tokenizer, tokens, context window, hallucination, hallucinations, ai hallucination, guardrails, benchmark, benchmarks, ai benchmark, agentic, agentic ai, ai agent, ai agents, autonomous agent, autonomous agents, multi-agent, mcp, model context protocol, tool use, function calling, openai, open ai, chatgpt, chat gpt, чатгпт, gpt, gpt-3, gpt-3.5, gpt-4, gpt-4o, gpt-4o mini, gpt-4.5, gpt-5, gpt-o1, gpt-o3, o1, o1-preview, o1-mini, o3, o3-mini, o4-mini, sora, dall-e, dall-e 2, dall-e 3, dalle, dalle2, dalle3, whisper, codex, openai codex, openai api, chatgpt plus, chatgpt pro, chatgpt enterprise, gpt store, custom gpt, gpts, openai playground, openai gym, clip, jukebox, point-e, shap-e, operator, anthropic, claude, claude 2, claude 3, claude 3.5, claude 3.7, claude 4, claude instant, claude 3.5 sonnet, claude 3.7 sonnet, claude opus, claude haiku, claude sonnet, claude code, клод, антропик, sonnet, opus, haiku, claude desktop, claude api, claude artifacts, constitutional ai, claude pro, claude max, google ai, google gemini, gemini, gemini pro, gemini ultra, gemini nano, gemini flash, gemini 1.5, gemini 2.0, gemini 2.5, bard, гугл джемини, google deepmind, deepmind, alphago, alphafold, alphacode, alphadev, alphageometry, palm, palm 2, palm-e, lamda, imagen, imagen 2, imagen 3, veo, veo 2, opal, genie, gemma, gemma 2, gemma 3, codegemma, recurrentgemma, google ai studio, vertex ai, google colab, tensorflow, keras, jax, tpu, google lens ai, notebooklm, notebook lm, google ai overviews, ai overviews, project astra, project mariner, jules, chirp, musiclm, soundstorm, meta ai, llama, llama 2, llama 3, llama 3.1, llama 3.2, llama 3.3, llama 4, codellama, code llama, лама, meta llama, segment anything, sam, sam 2, seamless, audibox, emu, emu video, emu edit, voicebox, musicgen, imagebind, chameleon, microsoft ai, microsoft copilot, copilot, github copilot, copilot studio, copilot+, copilot plus, azure ai, azure openai, azure cognitive services, bing ai, bing chat, phi, phi-2, phi-3, phi-4, orca, orca 2, deepspeed, lora, qlora, olive, semantic kernel, autogen, taskweaver, promptflow, midjourney, mid journey, мидджорни, миджорни, stable diffusion, stability ai, stabilityai, sdxl, sd 3, sd3, sd 3.5, stable cascade, comfyui, comfy ui, automatic1111, a1111, flux, flux.1, flux schnell, flux dev, flux pro, leonardo ai, ideogram, ideogram ai, firefly, adobe firefly, canva ai, playground ai, nightcafe, artbreeder, craiyon, bluewillow, fooocus, controlnet, img2img, txt2img, inpainting, outpainting, dreambooth, textual inversion, latent diffusion, diffusion model, diffusion models, image generation, ai art, ai-art, ии-арт, ai generated, ai-generated, runway, runway ml, runwayml, runway gen-2, runway gen-3, runway gen-4, kling, kling ai, luma, luma ai, luma dream machine, pika, pika labs, pika 1.0, pika 2.0, heygen, hey gen, хейджен, synthesia, d-id, did ai, invideo ai, vidu, minimax video, minimax, hailuo, hailuo ai, wan, wan 2.1, video generation, ai video, генерация видео, text to video, ai-видео, suno, suno ai, udio, elevenlabs, eleven labs, murf ai, murf.ai, bark, tortoise tts, coqui, resemble ai, play.ht, descript, aiva, soundraw, boomy, audiogen, stable audio, ai voice, ai music, ai-озвучка, ии-озвучка, клонирование голоса, голосовой клон, voice cloning, voice clone, ai voiceover, text to speech, tts, speech synthesis, синтез речи, cursor, cursor ide, курсор, devin, devin ai, v0, v0.dev, replit ai, replit agent, codeium, tabnine, amazon codewhisperer, codewhisperer, sourcegraph cody, cody ai, aider, aider chat, continue dev, supermaven, sweep ai, codium ai, qodo, windsurf, codeium windsurf, bolt, bolt.new, lovable, lovable dev, stackblitz ai, claude engineer, open interpreter, autogpt, auto-gpt, babyagi, agentgpt, crewai, crew ai, langchain, langchain ai, langgraph, llamaindex, llama index, dspy, haystack ai, vllm, ollama, lmstudio, lm studio, localai, jan ai, gpt4all, koboldcpp, textgenwebui, oobabooga, huggingface, hugging face, replicate, together ai, togetherai, groq, groqcloud, fireworks ai, anyscale, modal, openrouter, perplexity, perplexity ai, перплексити, you.com, phind, kagi ai, arc search, brave ai, brave search ai, pi ai, inflection ai, character ai, character.ai, chai ai, poe, poe.com, jasper ai, jasper, copy ai, writesonic, rytr, grammarly ai, notion ai, gamma ai, gamma app, beautiful ai, tome ai, tome app, mem ai, otter ai, fireflies ai, krisp, read ai, deepseek, deepseek v2, deepseek v3, deepseek r1, deepseek coder, qwen, qwen 2, qwen 2.5, qwen 3, tongyi qianwen, ernie, ernie bot, baidu ai, yi, yi-34b, 01.ai, zhipu ai, glm-4, chatglm, baichuan, internlm, mistral, mistral ai, mistral 7b, mixtral, mixtral 8x7b, mistral large, mistral medium, mistral small, le chat, lechat, grok, xai, x.ai, cohere, cohere ai, command r, command r+, ai21, ai21 labs, jurassic, jamba, reka, reka ai, databricks, dbrx, snowflake arctic, falcon, falcon 180b, tiiuae, nous hermes, wizardlm, wizard coder, openchat, starling, neural chat, solar, upstage, генерация, сгенерировать, сгенерировал, сгенерил, нагенерил, сгенерировано, сгенерированный, генеративный, дипфейк, deepfake, генерация картинок, генерация текста, ai-инструмент, ии-инструмент, ai-тулза, ai-тулзы, ии-тулзы, ai-ассистент, ии-ассистент, ai-помощник, ии-помощник, чат-бот, чатбот, ai-агент, автономные агенты, ии-агент, промпт, промпты, промптинг".split(",")]

def text_has_ai_topics(text: str) -> bool:
    if not text:
        return False
    text_lower = text.lower()
    text_words = set(re.findall(r'[\w]+', text_lower))
    for k in AI_KEYWORDS:
        if k in text_words:
            return True
        elif len(k) > 4 and k in text_lower:
            return True
        elif ' ' in k and k in text_lower:
            return True
        elif k == 'a.i.' and 'a.i.' in text_lower:
            return True
    return False


@dataclass
class PostFilter:
    """Server-side filter criteria applied during collection."""
    min_likes: int = 0
    max_likes: int = 0          # 0 = no upper limit
    min_comments: int = 0
    max_comments: int = 0       # 0 = no upper limit
    min_views: int = 0
    max_views: int = 0          # 0 = no upper limit
    max_followers: int = 0      # 0 = no upper limit (exclude millionaires)
    min_followers: int = 0
    max_age_hours: Optional[int] = None
    exclude_zero_engagement: bool = False  # skip posts with 0 likes AND 0 comments
    only_ai_topics: bool = False

    def matches(self, post: "PostData") -> bool:
        """Return True if the post passes all filter criteria."""
        # Date filter (Strict)
        if self.max_age_hours is not None and post.timestamp > 0:
            current_time = int(time.time())
            age_hours = (current_time - post.timestamp) / 3600
            if age_hours > self.max_age_hours:
                return False

        if self.exclude_zero_engagement and post.likes == 0 and post.comments == 0:
            return False
        if self.min_likes > 0 and post.likes < self.min_likes:
            return False
        if self.max_likes > 0 and post.likes > self.max_likes:
            return False
        if self.min_comments > 0 and post.comments < self.min_comments:
            return False
        if self.max_comments > 0 and post.comments > self.max_comments:
            return False
        if self.min_views > 0 and post.views < self.min_views:
            return False
        if self.max_views > 0 and post.views > self.max_views:
            return False
        if self.max_followers > 0 and post.owner_followers > self.max_followers:
            return False
        if self.min_followers > 0 and post.owner_followers < self.min_followers:
            return False
            
        # IA filter (Strict Text Matching)
        if self.only_ai_topics and not text_has_ai_topics(post.caption_text):
            return False
            
        return True


@dataclass
class PostData:
    """Normalised representation of an Instagram post."""
    post_id: str = ""
    shortcode: str = ""
    post_type: str = "unknown"
    owner_username: str = ""
    owner_full_name: str = ""
    owner_followers: int = 0
    caption_text: str = ""
    likes: int = 0
    comments: int = 0
    views: int = 0
    timestamp: int = 0
    url: str = ""
    thumbnail_url: str = ""
    is_reel: bool = False
    is_carousel: bool = False
    carousel_count: int = 0
    source: str = ""


@dataclass
class InterceptorState:
    """Accumulates captured posts across multiple scrolls."""
    posts: list[PostData] = field(default_factory=list)
    seen_ids: set[str] = field(default_factory=set)
    response_count: int = 0
    error_count: int = 0
    oldest_timestamp: int = 0
    filtered_out: int = 0
    reels_count: int = 0
    carousels_count: int = 0
    photos_count: int = 0

    def add_post(self, post: PostData, post_filter: Optional[PostFilter] = None) -> bool:
        """Add a post if not already seen and passes filters."""
        if post.post_id in self.seen_ids or not post.post_id:
            return False
        if post_filter and not post_filter.matches(post):
            self.filtered_out += 1
            return False
        self.seen_ids.add(post.post_id)
        self.posts.append(post)
        if post.is_reel:
            self.reels_count += 1
        elif post.is_carousel:
            self.carousels_count += 1
        else:
            self.photos_count += 1
        if post.timestamp > 0:
            if self.oldest_timestamp == 0:
                self.oldest_timestamp = post.timestamp
            else:
                self.oldest_timestamp = min(self.oldest_timestamp, post.timestamp)
        return True


# ── GraphQL response patterns we intercept ───────────

GRAPHQL_PATTERNS = [
    "graphql/query",
    "api/v1/feed/timeline",
    "api/v1/feed/reels_tray",
    "api/v1/discover/web/explore_grid",
    "api/v1/tags/",
    "api/v1/feed/tag/",
    "web_search_typeahead",
    "web/search/topsearch",
    "api/v1/clips/",
    "api/v1/fbsearch/",
    "api/v1/users/search/"
]


def _matches_ig_api(url: str) -> bool:
    return any(pat in url for pat in GRAPHQL_PATTERNS)


def _detect_post_type(node: dict) -> str:
    media_type = node.get("media_type")
    product_type = node.get("product_type", "")
    if product_type == "clips" or node.get("is_reel_media"):
        return "reel"
    typename = node.get("__typename", "")
    if typename in ("GraphSidecar", "XDTGraphSidecar") or node.get("carousel_media_count", 0) > 0:
        return "carousel"
    if media_type == 8:
        return "carousel"
    if media_type == 2:
        return "video"
    if media_type == 1:
        return "image"
    if typename == "GraphVideo" or node.get("is_video"):
        return "video"
    return "image"


def _safe_int(val: Any) -> int:
    if val is None:
        return 0
    try:
        v = int(val)
        return max(v, 0)
    except (ValueError, TypeError):
        return 0


def _extract_post(node: dict, source: str = "") -> Optional[PostData]:
    """Extract PostData from a single GraphQL media node."""
    try:
        post_id = str(node.get("pk", node.get("id", "")))
        shortcode = node.get("code", node.get("shortcode", ""))
        if not post_id and not shortcode:
            return None

        post_type = _detect_post_type(node)

        owner = node.get("owner", node.get("user", {})) or {}
        username = owner.get("username", "")
        full_name = owner.get("full_name", "")
        owner_followers = _safe_int(
            owner.get("follower_count")
            or owner.get("edge_followed_by", {}).get("count")
        )

        caption = ""
        cap_obj = node.get("caption")
        if isinstance(cap_obj, dict):
            caption = cap_obj.get("text", "")
        elif isinstance(cap_obj, str):
            caption = cap_obj
        if not caption:
            edges = node.get("edge_media_to_caption", {}).get("edges", [])
            if edges:
                caption = edges[0].get("node", {}).get("text", "")

        likes = _safe_int(
            node.get("like_count")
            or node.get("edge_media_preview_like", {}).get("count")
            or node.get("edge_liked_by", {}).get("count")
        )
        comments = _safe_int(
            node.get("comment_count")
            or node.get("edge_media_to_comment", {}).get("count")
            or node.get("edge_media_preview_comment", {}).get("count")
        )
        views = _safe_int(
            node.get("play_count")
            or node.get("video_view_count")
            or node.get("view_count")
        )
        timestamp = _safe_int(
            node.get("taken_at")
            or node.get("taken_at_timestamp")
            or node.get("device_timestamp")
        )

        url = f"https://www.instagram.com/p/{shortcode}/" if shortcode else ""
        if post_type == "reel" and shortcode:
            url = f"https://www.instagram.com/reel/{shortcode}/"

        thumb = (
            node.get("thumbnail_src")
            or node.get("display_url")
            or node.get("image_versions2", {}).get("candidates", [{}])[0].get("url", "")
            if isinstance(node.get("image_versions2"), dict) else ""
        )
        if not thumb:
            thumb = node.get("display_url", "")

        is_reel = post_type == "reel"
        is_carousel = post_type == "carousel"
        carousel_count = _safe_int(
            node.get("carousel_media_count")
            or len(node.get("edge_sidecar_to_children", {}).get("edges", []))
            or len(node.get("carousel_media", []))
        )

        return PostData(
            post_id=post_id, shortcode=shortcode, post_type=post_type,
            owner_username=username, owner_full_name=full_name,
            owner_followers=owner_followers,
            caption_text=caption[:500], likes=likes, comments=comments,
            views=views, timestamp=timestamp, url=url,
            thumbnail_url=thumb if isinstance(thumb, str) else "",
            is_reel=is_reel, is_carousel=is_carousel,
            carousel_count=carousel_count, source=source,
        )
    except Exception as exc:
        log.debug(f"Failed to extract post node: {exc}")
        return None


def _find_media_nodes(obj: Any, depth: int = 0, max_depth: int = 12) -> list[dict]:
    if depth > max_depth:
        return []
    results: list[dict] = []
    if isinstance(obj, dict):
        has_code = "shortcode" in obj or "code" in obj
        has_id = "pk" in obj or "id" in obj
        has_media = "media_type" in obj or "__typename" in obj or "taken_at" in obj or "taken_at_timestamp" in obj
        if has_code and has_id and has_media:
            results.append(obj)
        for v in obj.values():
            results.extend(_find_media_nodes(v, depth + 1, max_depth))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(_find_media_nodes(item, depth + 1, max_depth))
    return results


def extract_search_suggestions(data: dict) -> list[str]:
    suggestions: list[str] = []
    for ht in data.get("hashtags", []):
        name = ht.get("hashtag", {}).get("name", "")
        if name:
            suggestions.append(f"#{name}")
    for u in data.get("users", []):
        uname = u.get("user", u).get("username", "")
        if uname:
            suggestions.append(f"@{uname}")
    for p in data.get("places", []):
        title = p.get("place", p).get("title", "")
        if title:
            suggestions.append(title)
    return suggestions


async def handle_response(
    response,
    state: InterceptorState,
    source: str = "",
    fetch_images: bool = True,
    fetch_reels: bool = True,
    fetch_carousels: bool = True,
    post_filter: Optional[PostFilter] = None,
    progress_cb: Optional[Any] = None,
    global_state: Optional[InterceptorState] = None,
) -> None:
    """Callback for page.on('response'). Parses JSON and extracts posts."""
    url = response.url
    if not _matches_ig_api(url):
        return
    state.response_count += 1
    try:
        body = await response.body()
        text = body.decode("utf-8", errors="replace")
        if text.startswith("for (;;);"):
            text = text[len("for (;;);"):]
        data = json.loads(text)
    except Exception:
        state.error_count += 1
        return

    nodes = _find_media_nodes(data)
    added = 0
    for node in nodes:
        post = _extract_post(node, source=source)
        if post is None:
            continue
        if not fetch_images and post.post_type in ("image", "unknown", ""):
            continue
        if not fetch_reels and post.post_type in ("reel", "video"):
            continue
        if not fetch_carousels and post.post_type == "carousel":
            continue
        added_local = state.add_post(post, post_filter=post_filter)
        if global_state:
            global_state.add_post(post, post_filter=post_filter)
            
        if added_local:
            added += 1

    if added > 0 or len(nodes) > 0:
        log.info(f"[{source}] Found {len(nodes)} posts -> Added {added} (Total collected: {len(state.posts)}, Filtered out: {state.filtered_out}) from api endpoint")
        if progress_cb:
            cb_state = global_state if global_state else state
            try:
                progress_cb({
                    "collected": len(cb_state.posts),
                    "filtered": cb_state.filtered_out,
                    "reels": cb_state.reels_count,
                    "carousels": cb_state.carousels_count,
                    "photos": cb_state.photos_count
                })
            except Exception as e:
                log.debug(f"progress_cb error: {e}")
