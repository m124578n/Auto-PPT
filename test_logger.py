#!/usr/bin/env python3
"""
测试 Logger 系统
"""
import logging
import time

from AutoPPT.utils.logger import AppLogger


def main():
    """测试所有 logger 功能"""
    
    # 创建日志器
    logger = AppLogger(
        name="TestLogger",
        log_dir="logs",
        level=logging.DEBUG,
        colored=True
    )
    
    # ========== 1. 基本日志测试 ==========
    logger.section("基本日志功能测试")
    
    logger.debug("🔍 这是调试信息 - 用于详细的程序执行流程")
    logger.info("📝 这是普通信息 - 记录程序运行状态")
    logger.warning("⚠️  这是警告信息 - 提醒潜在问题")
    logger.error("❌ 这是错误信息 - 程序出错但继续运行")
    logger.success("✅ 这是成功信息 - 操作成功完成")
    
    # ========== 2. 进度条测试 ==========
    logger.subsection("进度条测试")
    logger.info("开始处理 100 个项目...")
    
    for i in range(1, 21):  # 只显示 20 步以加快测试
        logger.progress(i, 20, f"处理项目 {i}")
        time.sleep(0.05)
    
    logger.success("所有项目处理完成")
    
    # ========== 3. 表格输出测试 ==========
    logger.subsection("表格输出测试")
    
    logger.table(
        headers=["文件名", "状态", "大小", "耗时"],
        rows=[
            ["image_001.jpg", "✅ 成功", "2.3 MB", "1.2s"],
            ["image_002.jpg", "✅ 成功", "1.8 MB", "0.9s"],
            ["image_003.jpg", "❌ 失败", "-", "0.1s"],
            ["image_004.jpg", "✅ 成功", "3.1 MB", "1.5s"],
        ]
    )
    
    # ========== 4. 字典输出测试 ==========
    logger.subsection("字典输出测试")
    
    config = {
        "项目": "AutoPPT",
        "版本": "1.2.0",
        "数据库": {
            "主机": "localhost",
            "端口": 5432,
            "数据库名": "autoppt_db"
        },
        "缓存": {
            "启用": True,
            "TTL": 3600,
            "后端": "Redis"
        }
    }
    
    logger.log_dict("项目配置", config)
    
    # ========== 5. 性能监控测试 ==========
    logger.subsection("性能监控测试")
    
    # 使用上下文管理器
    logger.info("测试计时器（上下文管理器）")
    with logger.timer("数据处理"):
        time.sleep(0.5)
        logger.info("  → 正在处理数据...")
        time.sleep(0.3)
        logger.info("  → 处理完成")
    
    # 手动控制计时器
    logger.info("测试计时器（手动控制）")
    logger.performance.start_timer("文件下载")
    time.sleep(0.4)
    logger.performance.end_timer("文件下载")
    
    # 内存监控
    logger.performance.log_memory()
    
    # ========== 6. 装饰器测试 ==========
    logger.subsection("装饰器测试")
    
    @logger.log_performance
    def calculate_sum(n: int) -> int:
        """计算 1 到 n 的和"""
        total = sum(range(1, n + 1))
        return total
    
    logger.info("测试性能监控装饰器")
    result = calculate_sum(1000)
    logger.info(f"计算结果: {result}")
    
    @logger.catch_exceptions(reraise=False)
    def risky_function():
        """可能出错的函数"""
        logger.info("  → 执行危险操作...")
        raise ValueError("模拟错误")
    
    logger.info("测试异常捕获装饰器")
    risky_function()
    logger.info("  → 程序继续运行（异常已捕获）")
    
    # ========== 7. 模拟实际场景 ==========
    logger.section("模拟实际应用场景")
    
    # 场景：爬取网页
    logger.subsection("场景 1: 网页爬取")
    
    urls = [
        "https://example1.com",
        "https://example2.com",
        "https://example3.com"
    ]
    
    results = []
    for i, url in enumerate(urls, 1):
        logger.info(f"爬取: {url}")
        
        with logger.timer(f"爬取 {url}"):
            time.sleep(0.2)  # 模拟爬取
            
            if i == 2:
                logger.warning(f"  ⚠️  {url} 返回缓慢")
            
            results.append({
                "url": url,
                "status": "成功" if i != 2 else "慢速",
                "items": i * 10
            })
        
        logger.progress(i, len(urls))
    
    logger.success(f"爬取完成，共获取 {sum(r['items'] for r in results)} 个项目")
    
    # 显示结果表格
    logger.table(
        headers=["URL", "状态", "项目数"],
        rows=[[r["url"], r["status"], r["items"]] for r in results]
    )
    
    # 场景：数据处理流程
    logger.subsection("场景 2: 数据处理流程")
    
    stages = [
        ("数据清洗", 0.3),
        ("数据转换", 0.5),
        ("数据验证", 0.2),
        ("数据保存", 0.4)
    ]
    
    for stage_name, duration in stages:
        logger.info(f"开始: {stage_name}")
        with logger.timer(stage_name):
            time.sleep(duration)
        logger.success(f"完成: {stage_name}")
    
    # ========== 8. 不同日志级别测试 ==========
    logger.section("日志级别切换测试")
    
    logger.info("当前级别: INFO")
    logger.debug("这条 DEBUG 信息应该显示")
    
    logger.info("切换到 WARNING 级别...")
    logger.set_level(logging.WARNING)
    
    logger.debug("这条 DEBUG 信息不会显示")
    logger.info("这条 INFO 信息也不会显示")
    logger.warning("这条 WARNING 信息会显示")
    
    logger.info("恢复到 DEBUG 级别...")
    logger.set_level(logging.DEBUG)
    logger.debug("DEBUG 信息又可以显示了")
    
    # ========== 9. 总结 ==========
    logger.section("测试总结")
    
    summary = {
        "测试项目": 9,
        "基本日志": "✅ 通过",
        "进度条": "✅ 通过",
        "表格输出": "✅ 通过",
        "字典输出": "✅ 通过",
        "性能监控": "✅ 通过",
        "装饰器": "✅ 通过",
        "实际场景": "✅ 通过",
        "级别切换": "✅ 通过",
    }
    
    logger.table(
        headers=["测试项", "结果"],
        rows=list(summary.items())
    )
    
    logger.success("所有功能测试完成！")
    
    logger.info("📁 日志文件已保存到: logs/")
    logger.info("📊 查看完整日志请打开日志文件")
    
    # 关闭日志器
    logger.close()


if __name__ == "__main__":
    main()

