from typing import List, Any

class RecommendationEngine:
    """
    Dynamic AI Recommendation Engine for factory operations.
    Evaluates current metrics, predicted metrics, and health scores to generate
    actionable insights.
    """
    def generate(self, latest_record: Any, predicted_profit: float, health_score: float, health_category: str) -> List[str]:
        recommendations = []
        
        # Extract features
        sales = latest_record.sales
        production = latest_record.production
        electricity = latest_record.electricity_bill
        raw_material = latest_record.raw_material_cost
        salary = latest_record.salary
        inventory = latest_record.inventory
        running_hours = latest_record.machine_running_hours
        downtime = latest_record.machine_downtime
        profit = latest_record.profit

        # 1. Electricity Cost Recommendation
        if sales > 0 and (electricity / sales) > 0.12:
            recommendations.append(
                f"⚡ Reduce electricity usage: Electricity bill (${electricity:.2f}) represents a high percentage "
                f"({(electricity/sales)*100:.1f}%) of sales. Shift high-load processes to off-peak hours or audit machine efficiency."
            )

        # 2. Inventory Optimization Recommendation
        if sales > 0:
            inv_to_sales = inventory / sales
            if inv_to_sales > 0.8:
                recommendations.append(
                    f"📦 Optimize inventory purchases: Inventory (${inventory:.2f}) is high relative to sales. "
                    f"Hold off on raw material restocking to free up working capital."
                )
            elif inv_to_sales < 0.05:
                recommendations.append(
                    f"📦 Restock critical inventory: Inventory level (${inventory:.2f}) is low. "
                    f"Order raw materials soon to prevent sudden production stockouts."
                )
        else:
            if inventory > 5000:
                recommendations.append("📦 High inventory with zero sales recorded. Focus on selling existing stock before ordering more raw materials.")

        # 3. Machine Downtime & Maintenance Recommendation
        if downtime > 0:
            total_machine_time = running_hours + downtime
            downtime_ratio = downtime / total_machine_time if total_machine_time > 0 else 0
            if downtime_ratio > 0.15:
                recommendations.append(
                    f"🔧 Schedule immediate machine maintenance: Machine downtime is at {downtime:.1f} hours "
                    f"({downtime_ratio*100:.1f}% of total hours). Implement preventive maintenance."
                )
            elif downtime > 4.0:
                recommendations.append(
                    f"🔧 Plan machine checkup: Factory logged {downtime:.1f} hours of downtime today. "
                    f"Check calibration and inspect components to prevent breakdowns."
                )

        # 4. Expense Reduction Recommendation
        total_expenses = raw_material + salary + electricity
        if sales > 0 and total_expenses > sales:
            recommendations.append(
                f"💸 Reduce unnecessary expenses: Expenses (${total_expenses:.2f}) exceed sales (${sales:.2f}). "
                f"Renegotiate raw material contracts or audit operational overhead."
            )
        elif profit < 0:
            recommendations.append(
                f"💸 Expense Audit: Factory is operating at a net loss of ${abs(profit):.2f}. "
                f"Review administrative expenses, salaries, and utility contracts to restore positive cash flow."
            )

        # 5. Production Efficiency Recommendation
        if running_hours > 0:
            production_per_hour = production / running_hours
            # If machines are running long but output is low
            if production_per_hour < 2.0 and running_hours > 8.0:
                recommendations.append(
                    f"📈 Improve production efficiency: Output is low ({production_per_hour:.2f} units/hour) "
                    f"despite high machine operating hours ({running_hours:.1f} hrs). Check operator speed or machine speed calibration."
                )

        # 6. Market/Demand Capture Recommendation
        if predicted_profit > profit and (predicted_profit - profit) / (profit if profit != 0 else 1.0) > 0.20:
            recommendations.append(
                f"🚀 Increase production of high-demand products: ML models predict a future profit of "
                f"${predicted_profit:.2f} (current actual: ${profit:.2f}). Scale up operations to capture demand."
            )

        # 7. General Healthy Business Recommendation
        if health_category == "Excellent" and health_score > 90:
            recommendations.append("🌟 Business is in Excellent health! Consider reinvesting profits into factory expansion or technology upgrades.")
        elif len(recommendations) == 0:
            recommendations.append("✅ Operations are stable. Continue monitoring metrics daily and maintain scheduled preventative maintenance.")

        return recommendations
