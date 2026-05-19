import json
from openai import OpenAI
from config import MODELS, CATEGORIES

def analyze_submission(content: str, model_name: str) -> dict:
    model_config = MODELS[model_name]
    api_key = model_config.get("api_key", "")
    if not api_key:
        raise ValueError(f"未配置 {model_name} 的 API Key，请在环境变量中设置")
    client = OpenAI(api_key=api_key, base_url=model_config["base_url"])
    
    prompt = f"""你是一个社区投稿分析助手。请分析以下投稿内容，完成以下任务：

1. **事件分类**：从以下类别中选择最合适的一个：{', '.join(CATEGORIES)}
2. **生成标题**：用简短的一句话概括事件（10-20字）
3. **核心摘要**：将投稿浓缩为3-5句话的关键信息
4. **影响评估**：
   - 热度评分（1-10分），评分标准：
     * 1-3分：小范围影响，仅涉及少数人，传播性低
     * 4-5分：中等影响，有一定传播性，社区内可能关注
     * 6-7分：较大影响，涉及群体较多，容易引发讨论
     * 8-9分：重大影响，涉及面广，可能引发舆论热点
     * 10分：极重大影响，涉及公共利益、政策法规，可能引发社会关注
   - 评分理由（从影响人数、传播难度、类似事件先例、社会敏感度等角度分析）

请严格按照以下JSON格式返回，不要添加任何其他内容：
{{
    "title": "事件标题",
    "category": "分类",
    "summary": "核心摘要内容",
    "heat_score": 数字,
    "heat_reason": "评分理由"
}}

投稿内容：
{content}
"""
    
    response = client.chat.completions.create(
        model=model_config["model"],
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    result_text = response.choices[0].message.content.strip()
    
    try:
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        result = json.loads(result_text)
    except json.JSONDecodeError:
        result = {
            "title": "解析失败",
            "category": "其他",
            "summary": result_text,
            "heat_score": 5,
            "heat_reason": "AI返回格式异常，请查看原始摘要"
        }
    
    return result

def generate_report(content: str, analysis: dict) -> str:
    report = f"""# 投稿分析报告

## 事件标题
{analysis['title']}

## 事件类型
{analysis['category']}

## 核心摘要
{analysis['summary']}

## 影响评估
- **热度评分**：{analysis['heat_score']}/10
- **评分理由**：{analysis['heat_reason']}

---
*本报告由AI自动生成，仅供参考*
"""
    return report
