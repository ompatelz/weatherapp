"use client";

import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
} from "recharts";
import type { TrendPoint } from "@/types";

interface Props {
    data: TrendPoint[];
}

export default function TrendChart({ data }: Props) {
    return (
        <div className="w-full h-64">
            <ResponsiveContainer width="100%" height="100%">
                <LineChart
                    data={data}
                    margin={{ top: 5, right: 20, bottom: 5, left: 10 }}
                >
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis
                        dataKey="year"
                        tick={{ fill: "#94a3b8", fontSize: 12 }}
                        axisLine={{ stroke: "#475569" }}
                    />
                    <YAxis
                        tick={{ fill: "#94a3b8", fontSize: 12 }}
                        axisLine={{ stroke: "#475569" }}
                        tickFormatter={(v: number) =>
                            v >= 1000 ? `${(v / 1000).toFixed(0)}k` : String(v)
                        }
                    />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: "#1e293b",
                            border: "1px solid #334155",
                            borderRadius: "8px",
                            color: "#f1f5f9",
                        }}
                        formatter={(value: number | string | undefined) => [
                            `${Number(value ?? 0).toLocaleString()} MW`,
                            "Total Capacity",
                        ]}
                    />
                    <Line
                        type="monotone"
                        dataKey="total_capacity_mw"
                        stroke="#22d3ee"
                        strokeWidth={2.5}
                        dot={{
                            r: 4,
                            fill: "#22d3ee",
                            stroke: "#0e7490",
                            strokeWidth: 2,
                        }}
                        activeDot={{ r: 6 }}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
