from hello_agents import ToolRegistry
from tool_chan_mamager import ToolChain, ToolChainManager
from my_calculator_tool import my_calculator, create_calculator_registry


def test_mock_tool_chain():
    """测试场景 1：多步骤工具链数据透传 (搜索 -> 计算 -> 总结)"""
    print("\n" + "=" * 50)
    print("=== [Test 1] 模拟工具链透传测试 ===")
    print("=" * 50)

    # 1. 创建工具注册表
    registry = ToolRegistry()

    # 定义模拟工具
    def mock_search(query: str) -> str:
        return f"查询'{query}'得出数据：底边 length=10, 高 height=6"

    def mock_summarizer(text: str) -> str:
        return f"【最终汇报文档】\n{text}"

    registry.register_function("search", "搜索工具", mock_search)
    registry.register_function("summarizer", "总结报告生成工具", mock_summarizer)
    registry.register_function("my_calculator", "计算器工具", my_calculator)

    # 2. 构建多步骤工具链
    chain = ToolChain(
        name="triangle_area_pipeline",
        description="搜索三角形参数 -> 计算三角形面积 (0.5 * b * h) -> 格式化输出"
    )

    # 步骤 1：搜索数据
    chain.add_step(
        tool_name="search",
        input_template="{input}",
        output_key="search_res"
    )

    # 步骤 2：计算三角形面积 0.5 * 10 * 6
    chain.add_step(
        tool_name="my_calculator",
        input_template="0.5 * 10 * 6",
        output_key="calc_res"
    )

    # 步骤 3：总结与格式化
    chain.add_step(
        tool_name="summarizer",
        input_template="信息来源：[{search_res}]，计算得出的面积结果为：{calc_res}",
        output_key="final_report"
    )

    # 3. 管理器注册并运行
    manager = ToolChainManager(registry)
    manager.register_chain(chain)

    result = manager.execute_chain(
        chain_name="triangle_area_pipeline",
        input_data="三角形面积公式与参数"
    )

    print("\n[Result 1] 最终工具链执行结果：")
    print(result)


def test_custom_chain():
    """测试场景 2：动态创建简易工具链"""
    print("\n" + "=" * 50)
    print("=== [Test 2] 动态双步骤工具链测试 ===")
    print("=" * 50)

    registry = create_calculator_registry()

    # 简单工具链：计算 100 * 5 -> 再计算 sqrt(结果)
    chain = ToolChain(name="math_chain", description="连续数学运算链")
    chain.add_step("my_calculator", "100 * 5", output_key="step1")
    chain.add_step("my_calculator", "sqrt({step1})", output_key="step2")

    manager = ToolChainManager(registry)
    manager.register_chain(chain)

    result = manager.execute_chain("math_chain", input_data="")
    print("\n[Result 2] 连续运算结果：", result)


if __name__ == "__main__":
    test_mock_tool_chain()
    test_custom_chain()
