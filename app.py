"""
╔══════════════════════════════════════════════════════════════════╗
║         BIST SWING TRADE TARAYICI  —  Pro Edition v3            ║
║   Temel Analiz + Teknik Analiz + Grafikler + Gelişmiş Filtre   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime

# ══════════════════════════════════════════════════════════════════
# HİSSE LİSTESİ  (~220 BIST hissesi)
# ══════════════════════════════════════════════════════════════════
TICKERS = [
    "THYAO.IS","EREGL.IS","GARAN.IS","AKBNK.IS","YKBNK.IS","ISCTR.IS","KCHOL.IS",
    "SASA.IS","BIMAS.IS","FROTO.IS","TUPRS.IS","ASELS.IS","TOASO.IS","PGSUS.IS",
    "HALKB.IS","VAKBN.IS","TKFEN.IS","ENKAI.IS","KOZAL.IS","KRDMD.IS","PETKM.IS",
    "TTKOM.IS","TAVHL.IS","OTKAR.IS","SAHOL.IS","ARCLK.IS","VESTL.IS","MGROS.IS",
    "EKGYO.IS","ULKER.IS","TCELL.IS","SISE.IS","DOHOL.IS","AEFES.IS","LOGO.IS",
    "MAVI.IS","BRISA.IS","CCOLA.IS","ALARK.IS","AKSEN.IS","AYGAZ.IS","TSKB.IS",
    "SODA.IS","CIMSA.IS","OYAKC.IS","HEKTS.IS","DOAS.IS","TTRAK.IS","KARSN.IS",
    "ADEL.IS","NUHCM.IS","GUBRF.IS","LINK.IS","TRKCM.IS","AKGRT.IS","ANSGR.IS",
    "AGESA.IS","ALKIM.IS","SARKY.IS","KUTPO.IS","ERBOS.IS","DMSAS.IS","KAPLM.IS",
    "CLEBI.IS","YATAS.IS","MPARK.IS","ODAS.IS","BERA.IS","INDES.IS","OBASE.IS",
    "SKBNK.IS","KLNMA.IS","ISGYO.IS","RYGYO.IS","DZGYO.IS","TRGYO.IS","VKGYO.IS",
    "KOZAA.IS","KRDMA.IS","KRDMB.IS","GEREL.IS","SODSN.IS","BANVT.IS","AVOD.IS",
    "PKART.IS","SANEL.IS","KATMR.IS","FONET.IS","KAREL.IS","SOKM.IS","TBORG.IS",
    "GWIND.IS","ENERY.IS","EUPWR.IS","BOSSA.IS","CELHA.IS","EGEEN.IS","GOODY.IS",
    "HATEK.IS","IHLAS.IS","JANTS.IS","KORDS.IS","KRSAN.IS","PETUN.IS","PINSU.IS",
    "SANFM.IS","SEKUR.IS","TATGD.IS","TMSN.IS","TUKAS.IS","ULUUN.IS","UNLU.IS",
    "YAPRK.IS","YUNSA.IS","AAIGM.IS","ACSEL.IS","AKBLK.IS","ALFAS.IS","ALVES.IS",
    "ANELE.IS","ARDYZ.IS","ARENA.IS","ARSAN.IS","AVGYO.IS","AZTEK.IS","BAKAB.IS",
    "BALAT.IS","BARMA.IS","BEGYO.IS","BFREN.IS","BIGCH.IS","BLCYT.IS","BMSTL.IS",
    "BRKSN.IS","BRSAN.IS","BURCE.IS","BURVA.IS","CEMAS.IS","CEOEM.IS","COMDO.IS",
    "COSMO.IS","CUSAN.IS","CWENE.IS","DATA.IS","DERHL.IS","DESA.IS","DESPC.IS",
    "DEVA.IS","DITAS.IS","DNISI.IS","DOBUR.IS","DURDO.IS","DYOBY.IS","ECILC.IS",
    "ECZYT.IS","EDIP.IS","EGEPO.IS","EGSER.IS","EMKEL.IS","EMNIS.IS","ENPLA.IS",
    "EPLAS.IS","ERSU.IS","ESCOM.IS","ETILR.IS","EUHOL.IS","EURO.IS","EUROB.IS",
    "FBASE.IS","FENER.IS","FORMT.IS","FORTE.IS","FRIGO.IS","GEDIK.IS","GESAN.IS",
    "GLBMD.IS","GOLDS.IS","GRNYO.IS","GRSEL.IS","GSDDE.IS","GSDHO.IS","GSRAY.IS",
    "GULFA.IS","GVENS.IS","HTTBT.IS","HUNER.IS","HURGZ.IS","ICBCT.IS","IHLGM.IS",
    "IHEVA.IS","ISATR.IS","ISKPL.IS","ISKUR.IS","ISYAT.IS","ITTFH.IS","IZTAR.IS",
    "KFEIN.IS","KONTR.IS","KONYA.IS","KRPLA.IS","KRVGD.IS","KSTUR.IS","KTLEV.IS",
    "KTSKR.IS","KWPWR.IS","LIDER.IS","LKMNH.IS","MEMSA.IS","MEGES.IS","MOBTL.IS",
    "MRSHL.IS","NTGAZ.IS","NUGYO.IS","OSMEN.IS","OZBAL.IS","PENGD.IS","PKENT.IS",
    "PRZMA.IS","QNBFB.IS","QNBFL.IS","RUBNS.IS","SAMAT.IS","SANKO.IS","SEGYO.IS",
    "SEKFK.IS","SELGD.IS","SEZGI.IS","SILVR.IS","SKYLP.IS","TEBNK.IS","TMPOL.IS",
    "TREYD.IS","TUCLK.IS","TUMTK.IS","UZERB.IS","VERUS.IS","VKING.IS","YESIL.IS",
    "YGGYO.IS","YKSGR.IS","ZEDUR.IS","BJKAS.IS","EKIZ.IS","IHGZT.IS",
    "TSPOR.IS","SELEC.IS","GOLTS.IS","ISGSY.IS","ISDMR.IS","KOZA1.IS",
    "ALTNY.IS","DMRGD.IS","PRKME.IS","FADE.IS","ARAT.IS","DENGE.IS","NETAS.IS",
]
TICKERS = list(dict.fromkeys(TICKERS))

# ══════════════════════════════════════════════════════════════════
# TEKNİK GÖSTERGE HESAPLAMALARI
# ══════════════════════════════════════════════════════════════════

def calc_rsi(close: pd.Series, period=14) -> pd.Series:
    delta = close.diff()
    gain  = delta.clip(lower=0).ewm(alpha=1/period, min_periods=period).mean()
    loss  = (-delta.clip(upper=0)).ewm(alpha=1/period, min_periods=period).mean()
    rs    = gain / loss.replace(0, np.nan)
    return 100 - 100 / (1 + rs)

def calc_macd(close: pd.Series):
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    line  = ema12 - ema26
    sig   = line.ewm(span=9, adjust=False).mean()
    hist  = line - sig
    return line, sig, hist

def calc_atr(high, low, close, period=14) -> pd.Series:
    prev = close.shift(1)
    tr   = pd.concat([high-low, (high-prev).abs(), (low-prev).abs()], axis=1).max(axis=1)
    return tr.ewm(span=period, adjust=False).mean()

def calc_bollinger(close: pd.Series, period=20):
    ma  = close.rolling(period).mean()
    std = close.rolling(period).std()
    return ma, ma + 2*std, ma - 2*std

# ══════════════════════════════════════════════════════════════════
# TEK HİSSE ANALİZ & PUANLAMA
# ══════════════════════════════════════════════════════════════════

def analyze(ticker: str, fund_timeout=6) -> dict | None:
    try:
        # ── Fiyat Verisi ──────────────────────────────────────────
        raw = yf.download(ticker, period="1y", interval="1d",
                          auto_adjust=True, progress=False, timeout=10)
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)
        df = raw[["Close","High","Low","Volume"]].dropna()
        if len(df) < 60:
            return None

        close = df["Close"].squeeze()
        high  = df["High"].squeeze()
        low   = df["Low"].squeeze()
        vol   = df["Volume"].squeeze()
        price = float(close.iloc[-1])

        # ── Hareketli Ortalamalar ─────────────────────────────────
        ma20  = close.rolling(20).mean()
        ma50  = close.rolling(50).mean()
        ma200 = close.rolling(200).mean()
        ma50v  = float(ma50.iloc[-1])
        ma200v = float(ma200.iloc[-1]) if not np.isnan(ma200.iloc[-1]) else None

        above_ma50  = price > ma50v
        above_ma200 = (ma200v is None) or (price > ma200v)

        if not (above_ma50 and above_ma200):
            return {"ticker": ticker, "toplam": 0, "elendi": "MA50/MA200 Altı"}

        # ── Teknik Göstergeler ────────────────────────────────────
        rsi_s        = calc_rsi(close)
        rsi_val      = float(rsi_s.iloc[-1])

        macd_l, macd_sig, macd_hist = calc_macd(close)
        m_h          = float(macd_hist.iloc[-1])
        m_hp         = float(macd_hist.iloc[-2]) if len(macd_hist) > 1 else 0.0
        m_line       = float(macd_l.iloc[-1])
        m_sig        = float(macd_sig.iloc[-1])

        atr_s        = calc_atr(high, low, close)
        atr_val      = float(atr_s.iloc[-1])
        atr_pct      = (atr_val / price) * 100

        boll_mid, boll_up, boll_dn = calc_bollinger(close)
        boll_mid_v   = float(boll_mid.iloc[-1])
        boll_up_v    = float(boll_up.iloc[-1])
        boll_dn_v    = float(boll_dn.iloc[-1])
        boll_pos     = (price - boll_dn_v) / (boll_up_v - boll_dn_v) if (boll_up_v - boll_dn_v) != 0 else 0.5

        vol5         = float(vol.iloc[-5:].mean())
        vol20        = float(vol.iloc[-20:].mean())
        vol_ratio    = vol5 / vol20 if vol20 > 0 else 1.0

        # Fiyat momentumu: son 5 günlük değişim
        mom5         = ((price - float(close.iloc[-6])) / float(close.iloc[-6])) * 100 if len(close) > 6 else 0.0
        mom20        = ((price - float(close.iloc[-21])) / float(close.iloc[-21])) * 100 if len(close) > 21 else 0.0

        # ── Temel Analiz Verisi ───────────────────────────────────
        # Kısa timeout ile bilgi çek, yoksa nötr puan
        pe, pb, earn_g, rev_g, profit_m, debt_eq = None, None, None, None, None, None
        sector = "—"
        try:
            info    = yf.Ticker(ticker).fast_info
            t_full  = yf.Ticker(ticker)
            idict   = t_full.info or {}
            pe      = idict.get("trailingPE") or idict.get("forwardPE")
            pb      = idict.get("priceToBook")
            earn_g  = idict.get("earningsQuarterlyGrowth")   # çeyreklik YoY
            rev_g   = idict.get("revenueGrowth")
            profit_m= idict.get("profitMargins")
            debt_eq = idict.get("debtToEquity")
            sector  = idict.get("sector", "—") or "—"
        except Exception:
            pass

        # ══════════════════════════════════════════════════════════
        # PUANLAMA  ─  Toplam 100 Puan
        # TEKNİK : 65 puan  |  TEMEL : 35 puan
        # ══════════════════════════════════════════════════════════

        # ── A. TEKNİK (65) ──────────────────────────────────────

        # A1. RSI (0-20)
        if   rsi_val < 30:         rsi_p = 3
        elif rsi_val < 42:         rsi_p = 10
        elif rsi_val < 50:         rsi_p = 15
        elif rsi_val <= 63:        rsi_p = 20   # altın bölge
        elif rsi_val <= 70:        rsi_p = 15
        elif rsi_val <= 78:        rsi_p = 7
        else:                      rsi_p = 2

        # A2. MACD (0-20)
        guclu   = m_h > 0 and m_h > m_hp and m_line > m_sig
        buyuyor = m_h > 0 and m_h > m_hp
        if   guclu:                macd_p = 20
        elif buyuyor:              macd_p = 15
        elif m_h > 0:              macd_p = 10
        elif m_line > m_sig:       macd_p = 6
        else:                      macd_p = 0

        # A3. Hacim (0-12)
        if   vol_ratio > 2.5:      vol_p = 12
        elif vol_ratio > 1.8:      vol_p = 10
        elif vol_ratio > 1.3:      vol_p = 7
        elif vol_ratio >= 1.0:     vol_p = 4
        else:                      vol_p = 0

        # A4. ATR Volatilite (0-8)
        if   atr_pct < 0.8:        atr_p = 1
        elif atr_pct < 1.5:        atr_p = 4
        elif atr_pct <= 3.5:       atr_p = 8   # ideal swing
        elif atr_pct <= 5.5:       atr_p = 5
        elif atr_pct <= 7.5:       atr_p = 2
        else:                      atr_p = 0

        # A5. Bollinger Pozisyonu (0-5)
        # %20-70 arası bant içi → ideal, çok uçlarda ceza
        if   0.20 <= boll_pos <= 0.70:  boll_p = 5
        elif 0.10 <= boll_pos < 0.20:   boll_p = 3
        elif 0.70 < boll_pos <= 0.85:   boll_p = 2
        else:                            boll_p = 0

        # A6. MA Trend Bonus (0-5) — MA50 > MA200 golden cross yapısı
        ma_p = 0
        if ma200v and ma50v > ma200v:        ma_p += 3
        ma50_dist = ((price - ma50v) / ma50v) * 100
        if 1 <= ma50_dist <= 12:             ma_p += 2

        teknik_p = min(rsi_p + macd_p + vol_p + atr_p + boll_p + ma_p, 65)

        # ── B. TEMEL (35) ────────────────────────────────────────

        # B1. F/K — Fiyat/Kazanç (0-12)
        pe_p = 6  # veri yoksa nötr
        if pe is not None and pe > 0:
            if   pe < 5:     pe_p = 12   # çok ucuz
            elif pe < 10:    pe_p = 10
            elif pe < 15:    pe_p = 8
            elif pe < 20:    pe_p = 6
            elif pe < 30:    pe_p = 3
            else:            pe_p = 0   # pahalı

        # B2. PD/DD — Fiyat/Defter (0-10)
        pb_p = 5  # veri yoksa nötr
        if pb is not None and pb > 0:
            if   pb < 0.8:   pb_p = 10  # defter değerinin altında
            elif pb < 1.5:   pb_p = 8
            elif pb < 2.5:   pb_p = 6
            elif pb < 4.0:   pb_p = 3
            else:            pb_p = 0

        # B3. Kazanç Büyümesi YoY (0-8)
        eg_p = 4  # veri yoksa nötr
        if earn_g is not None:
            if   earn_g > 0.50:   eg_p = 8
            elif earn_g > 0.25:   eg_p = 6
            elif earn_g > 0.10:   eg_p = 5
            elif earn_g > 0:      eg_p = 3
            else:                 eg_p = 0  # kar düşüşü

        # B4. Net Kar Marjı (0-5)
        pm_p = 2  # nötr
        if profit_m is not None:
            if   profit_m > 0.25:  pm_p = 5
            elif profit_m > 0.15:  pm_p = 4
            elif profit_m > 0.08:  pm_p = 3
            elif profit_m > 0:     pm_p = 1
            else:                  pm_p = 0

        temel_p = min(pe_p + pb_p + eg_p + pm_p, 35)

        toplam = round(min(teknik_p + temel_p, 100), 1)

        # MACD etiketi
        if   guclu:       macd_lbl = "🔥 Güçlü Al"
        elif buyuyor:     macd_lbl = "📈 Büyüyor"
        elif m_h > 0:     macd_lbl = "✅ Pozitif"
        else:             macd_lbl = "❌ Negatif"

        return {
            # Kimlik
            "ticker":    ticker,
            "sektor":    sector,
            # Fiyat
            "fiyat":     round(price, 2),
            "ma50":      round(ma50v, 2),
            "ma200":     round(ma200v, 2) if ma200v else None,
            "mom5":      round(mom5, 2),
            "mom20":     round(mom20, 2),
            # Skorlar
            "toplam":    toplam,
            "teknik_p":  teknik_p,
            "temel_p":   temel_p,
            # Teknik detay
            "rsi":       round(rsi_val, 1),
            "rsi_p":     rsi_p,
            "macd_lbl":  macd_lbl,
            "macd_p":    macd_p,
            "vol_ratio": round(vol_ratio, 2),
            "vol_p":     vol_p,
            "atr_pct":   round(atr_pct, 2),
            "atr_p":     atr_p,
            "boll_pos":  round(boll_pos * 100, 1),
            "boll_p":    boll_p,
            "ma_p":      ma_p,
            # Temel detay
            "pe":        round(pe, 2) if pe else None,
            "pe_p":      pe_p,
            "pb":        round(pb, 2) if pb else None,
            "pb_p":      pb_p,
            "earn_g":    round(earn_g*100, 1) if earn_g else None,
            "eg_p":      eg_p,
            "profit_m":  round(profit_m*100, 1) if profit_m else None,
            "pm_p":      pm_p,
            # Seri (grafik için)
            "_close":    close,
            "_high":     high,
            "_low":      low,
            "_vol":      vol,
            "_rsi":      rsi_s,
            "_macd_l":   macd_l,
            "_macd_sig": macd_sig,
            "_macd_hist":macd_hist,
            "_ma20":     ma20,
            "_ma50":     ma50,
            "_ma200":    ma200,
            "_boll_up":  boll_up,
            "_boll_dn":  boll_dn,
            "_atr":      atr_s,
            "elendi":    None,
        }

    except Exception:
        return None


# ══════════════════════════════════════════════════════════════════
# GRAFİK FONKSİYONU  — Seçilen hisse için detay grafik
# ══════════════════════════════════════════════════════════════════

def draw_chart(row: dict):
    close = row["_close"]
    high  = row["_high"]
    low   = row["_low"]
    vol   = row["_vol"]
    dates = close.index

    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        row_heights=[0.45, 0.18, 0.18, 0.19],
        vertical_spacing=0.03,
        subplot_titles=("Fiyat + MA + Bollinger", "Hacim", "RSI", "MACD")
    )

    # ── Panel 1: Mum + MA + Bollinger ─────────────────────────────
    fig.add_trace(go.Candlestick(
        x=dates, open=close.shift(1), high=high, low=low, close=close,
        name="Fiyat", increasing_fillcolor="#26a69a", decreasing_fillcolor="#ef5350",
        increasing_line_color="#26a69a", decreasing_line_color="#ef5350",
        showlegend=False
    ), row=1, col=1)

    for serie, label, color, width in [
        (row["_ma20"],    "MA20",  "#f9c74f", 1.2),
        (row["_ma50"],    "MA50",  "#4A90D9", 1.5),
        (row["_ma200"],   "MA200", "#e05c5c", 1.5),
        (row["_boll_up"], "BB Üst","#aaa",    1),
        (row["_boll_dn"], "BB Alt","#aaa",    1),
    ]:
        fig.add_trace(go.Scatter(
            x=dates, y=serie, name=label,
            line=dict(color=color, width=width, dash="dot" if "BB" in label else "solid"),
            opacity=0.85
        ), row=1, col=1)

    # ── Panel 2: Hacim ────────────────────────────────────────────
    vol_colors = ["#26a69a" if close.iloc[i] >= close.iloc[i-1] else "#ef5350"
                  for i in range(len(close))]
    fig.add_trace(go.Bar(
        x=dates, y=vol, name="Hacim",
        marker_color=vol_colors, showlegend=False
    ), row=2, col=1)

    vol20_line = vol.rolling(20).mean()
    fig.add_trace(go.Scatter(
        x=dates, y=vol20_line, name="Vol MA20",
        line=dict(color="#f9c74f", width=1.2)
    ), row=2, col=1)

    # ── Panel 3: RSI ─────────────────────────────────────────────
    rsi_s = row["_rsi"]
    fig.add_trace(go.Scatter(
        x=dates, y=rsi_s, name="RSI",
        line=dict(color="#ab63fa", width=1.5)
    ), row=3, col=1)

    for lvl, color in [(70,"#ef5350"), (30,"#26a69a"), (50,"#555")]:
        fig.add_hline(y=lvl, line_dash="dash", line_color=color,
                      line_width=0.8, row=3, col=1)

    # RSI bölge renklendirmesi
    fig.add_hrect(y0=50, y1=70, fillcolor="rgba(38,166,154,0.08)",
                  line_width=0, row=3, col=1)
    fig.add_hrect(y0=0, y1=30, fillcolor="rgba(239,83,80,0.08)",
                  line_width=0, row=3, col=1)

    # ── Panel 4: MACD ─────────────────────────────────────────────
    macd_l   = row["_macd_l"]
    macd_sig = row["_macd_sig"]
    macd_h   = row["_macd_hist"]

    hist_colors = ["#26a69a" if v >= 0 else "#ef5350" for v in macd_h]
    fig.add_trace(go.Bar(
        x=dates, y=macd_h, name="Histogram",
        marker_color=hist_colors, showlegend=False, opacity=0.7
    ), row=4, col=1)
    fig.add_trace(go.Scatter(
        x=dates, y=macd_l, name="MACD",
        line=dict(color="#4A90D9", width=1.4)
    ), row=4, col=1)
    fig.add_trace(go.Scatter(
        x=dates, y=macd_sig, name="Sinyal",
        line=dict(color="#f9c74f", width=1.4)
    ), row=4, col=1)
    fig.add_hline(y=0, line_color="#555", line_width=0.8, row=4, col=1)

    # ── Layout ───────────────────────────────────────────────────
    fig.update_layout(
        height=720,
        plot_bgcolor="#0f1117",
        paper_bgcolor="#0f1117",
        font=dict(color="#e0e0e0", size=11),
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", y=1.04, x=0, font_size=10),
        margin=dict(l=10, r=10, t=50, b=10),
        title=dict(
            text=f"<b>{row['ticker']}</b>  —  Fiyat: {row['fiyat']} ₺  |  "
                 f"Skor: {row['toplam']}/100  |  RSI: {row['rsi']}  |  {row['macd_lbl']}",
            font=dict(size=14)
        )
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#1e2530", zeroline=False)

    return fig


# ══════════════════════════════════════════════════════════════════
# SKOR RADAR GRAFİĞİ — Hisse detay kartı için
# ══════════════════════════════════════════════════════════════════

def draw_radar(row: dict):
    cats = ["RSI", "MACD", "Hacim", "ATR", "Bollinger", "F/K", "PD/DD", "Kar Büyüme", "Kar Marjı"]
    vals = [
        row["rsi_p"],  row["macd_p"], row["vol_p"],
        row["atr_p"],  row["boll_p"], row["pe_p"],
        row["pb_p"],   row["eg_p"],   row["pm_p"],
    ]
    maxs = [20, 20, 12, 8, 5, 12, 10, 8, 5]
    norm = [v/m*100 for v, m in zip(vals, maxs)]

    fig = go.Figure(go.Scatterpolar(
        r=norm + [norm[0]],
        theta=cats + [cats[0]],
        fill="toself",
        fillcolor="rgba(74,144,217,0.25)",
        line=dict(color="#4A90D9", width=2),
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0,100],
                            tickfont=dict(size=8), gridcolor="#2a3040"),
            angularaxis=dict(tickfont=dict(size=10)),
            bgcolor="#0f1117"
        ),
        paper_bgcolor="#0f1117",
        font=dict(color="#e0e0e0"),
        margin=dict(l=30, r=30, t=30, b=10),
        height=300,
        showlegend=False,
    )
    return fig


# ══════════════════════════════════════════════════════════════════
# STREAMLIT SAYFALARI
# ══════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="BIST Swing Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
.main { background-color: #0f1117; }
.metric-card {
    background: #1e2530; border-radius: 12px; padding: 16px 20px;
    border-left: 4px solid #4A90D9; margin-bottom: 8px;
}
.score-high  { color: #26a69a; font-size: 28px; font-weight: 800; }
.score-mid   { color: #f9c74f; font-size: 28px; font-weight: 800; }
.score-low   { color: #ef5350; font-size: 28px; font-weight: 800; }
div[data-testid="stMetricValue"] { font-size: 28px !important; }
</style>
""", unsafe_allow_html=True)

# ── Başlık ───────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(90deg,#1a2744,#0f1117);
            padding:20px 28px;border-radius:12px;margin-bottom:20px;
            border-left:5px solid #4A90D9;">
<h2 style="margin:0;color:#e0e0e0;">📈 BIST Swing Trade Tarayıcı  <span style="font-size:14px;color:#888;">Pro Edition v3</span></h2>
<p style="margin:6px 0 0;color:#aaa;font-size:13px;">
Temel Analiz + Teknik Analiz  •  100 Puan Sistemi  •  1 Aylık Swing Trade Odaklı
</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Tarama Ayarları")

    n_hisse   = st.slider("Taranacak Hisse Sayısı", 30, len(TICKERS), 200, 10)
    gecikme   = st.slider("İstek Gecikmesi (sn)", 0.1, 1.0, 0.3, 0.05,
                          help="yfinance rate-limit koruması için")
    min_skor  = st.slider("Minimum AL Skoru /100", 40, 90, 65, 5)

    st.markdown("---")
    st.markdown("### 🔬 Teknik Filtreler")
    rsi_min   = st.slider("RSI Alt Sınır",   0,  50,  38)
    rsi_max   = st.slider("RSI Üst Sınır",  50, 100,  75)
    vol_min   = st.slider("Min Hacim Ort. (5g/20g)", 0.5, 3.0, 1.0, 0.1)
    atr_min   = st.slider("Min ATR %", 0.0, 5.0, 0.8, 0.1)
    atr_max   = st.slider("Max ATR %", 1.0, 15.0, 7.0, 0.5)

    st.markdown("---")
    st.markdown("### 📊 Temel Filtreler")
    pe_max    = st.slider("Max F/K  (0 = filtre yok)", 0, 100, 30)
    pb_max    = st.slider("Max PD/DD (0 = filtre yok)", 0, 20, 6)
    mom5_min  = st.slider("Min 5 Günlük Momentum %", -10.0, 10.0, -3.0, 0.5)

    st.markdown("---")
    st.markdown("### 📋 Görünüm")
    show_elim = st.checkbox("Elenen hisseleri göster", False)
    basla     = st.button("🚀 Taramayı Başlat", type="primary", use_container_width=True)

# ── SESSION STATE ─────────────────────────────────────────────────
if "sonuclar" not in st.session_state:
    st.session_state.sonuclar  = []
    st.session_state.elenenler = []
    st.session_state.tarama_ok = False

# ══════════════════════════════════════════════════════════════════
# TARAMA
# ══════════════════════════════════════════════════════════════════
if basla:
    taranacak = TICKERS[:n_hisse]
    sonuclar, elenenler, hatalar = [], [], 0

    prog  = st.progress(0, text="Başlatılıyor...")
    durum = st.empty()

    for i, tkr in enumerate(taranacak):
        durum.markdown(
            f"<span style='color:#888'>⏳ Taranan:</span> **{tkr}**  "
            f"<span style='color:#555'>({i+1}/{len(taranacak)})</span>",
            unsafe_allow_html=True
        )
        r = analyze(tkr)

        if r is None:
            hatalar += 1
        elif r.get("elendi"):
            elenenler.append(r)
        else:
            sonuclar.append(r)

        prog.progress((i+1) / len(taranacak))
        time.sleep(gecikme)

    prog.empty()
    durum.empty()

    st.session_state.sonuclar  = sonuclar
    st.session_state.elenenler = elenenler
    st.session_state.hatalar   = hatalar
    st.session_state.tarama_ok = True

# ══════════════════════════════════════════════════════════════════
# SONUÇLAR
# ══════════════════════════════════════════════════════════════════
if st.session_state.tarama_ok:
    sonuclar  = st.session_state.sonuclar
    elenenler = st.session_state.elenenler
    hatalar   = st.session_state.get("hatalar", 0)

    if not sonuclar:
        st.error("Hiç sonuç alınamadı. Gecikmeyi artırıp tekrar deneyin.")
        st.stop()

    df_raw = pd.DataFrame(sonuclar).sort_values("toplam", ascending=False).reset_index(drop=True)

    # ── Filtreleri Uygula ────────────────────────────────────────
    df = df_raw.copy()
    df = df[(df["rsi"] >= rsi_min) & (df["rsi"] <= rsi_max)]
    df = df[(df["vol_ratio"] >= vol_min)]
    df = df[(df["atr_pct"] >= atr_min) & (df["atr_pct"] <= atr_max)]
    df = df[df["mom5"] >= mom5_min]
    if pe_max > 0:
        df = df[(df["pe"].isna()) | (df["pe"] <= pe_max)]
    if pb_max > 0:
        df = df[(df["pb"].isna()) | (df["pb"] <= pb_max)]

    df_al = df[df["toplam"] >= min_skor].reset_index(drop=True)

    # ── Özet Metrikler ───────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🔍 Taranan",       len(TICKERS[:n_hisse]))
    c2.metric("📊 Trend Üstü",    len(sonuclar))
    c3.metric("✅ Filtreyi Geçen", len(df))
    c4.metric("🚀 AL Listesi",    len(df_al))
    c5.metric("⚠️ Elenen/Hata",  f"{len(elenenler)}/{hatalar}")

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # TAB YAPISI
    # ══════════════════════════════════════════════════════════════
    tab1, tab2, tab3, tab4 = st.tabs([
        "🚀 AL Listesi", "📊 Grafikler & Analiz", "🗂 Tüm Sonuçlar", "📖 Sistem Hakkında"
    ])

    # ════════════════════════════
    # TAB 1 — AL LİSTESİ
    # ════════════════════════════
    with tab1:
        st.subheader(f"🚀 AL Listesi — {len(df_al)} hisse  (≥{min_skor} puan)")

        if df_al.empty:
            st.warning("Filtreyi karşılayan hisse bulunamadı. Sidebar'dan filtreleri gevşetin.")
        else:
            # ── Top 5 Kartları ───────────────────────────────────
            top5 = df_al.head(5)
            cols = st.columns(min(5, len(top5)))
            emojiler = ["🥇","🥈","🥉","4️⃣","5️⃣"]

            for idx, (_, row) in enumerate(top5.iterrows()):
                brd   = "#26a69a" if row["toplam"] >= 75 else "#4A90D9" if row["toplam"] >= 65 else "#f9c74f"
                s_cls = "score-high" if row["toplam"] >= 75 else "score-mid" if row["toplam"] >= 65 else "score-low"
                pe_s  = f"{row['pe']}" if row["pe"] else "—"
                pb_s  = f"{row['pb']}" if row["pb"] else "—"
                eg_s  = f"%{row['earn_g']}" if row["earn_g"] else "—"
                cols[idx].markdown(f"""
<div style="background:#1a2030;padding:14px;border-radius:12px;
            border-top:3px solid {brd};font-size:12.5px;line-height:2.0;">
<div style="font-size:18px;font-weight:700;color:#e0e0e0;">{emojiler[idx]} {row['ticker']}</div>
<span class="{s_cls}">{row['toplam']}</span><span style="color:#666;font-size:12px;">/100</span><br>
💰 <b>{row['fiyat']} ₺</b><br>
📊 RSI: {row['rsi']}  {row['macd_lbl']}<br>
📦 Hacim: ×{row['vol_ratio']}<br>
🎯 ATR: %{row['atr_pct']}<br>
📈 5g Momentum: %{row['mom5']}<br>
<hr style="border-color:#2a3040;margin:6px 0;">
F/K: {pe_s}  |  PD/DD: {pb_s}  |  Kar↑: {eg_s}<br>
Sektör: <i>{row['sektor']}</i>
</div>""", unsafe_allow_html=True)

            st.markdown("---")

            # ── Ana Tablo ─────────────────────────────────────────
            kolon_map = {
                "ticker":    "Hisse",
                "sektor":    "Sektör",
                "fiyat":     "Fiyat ₺",
                "toplam":    "Skor /100",
                "teknik_p":  "Teknik /65",
                "temel_p":   "Temel /35",
                "rsi":       "RSI",
                "macd_lbl":  "MACD",
                "vol_ratio": "Hacim Ort.",
                "atr_pct":   "ATR %",
                "boll_pos":  "Boll. Pos %",
                "mom5":      "Momentum 5g %",
                "mom20":     "Momentum 20g %",
                "pe":        "F/K",
                "pb":        "PD/DD",
                "earn_g":    "Kar Büy. %",
                "profit_m":  "Kar Marjı %",
                "ma50":      "MA50",
                "ma200":     "MA200",
            }
            df_goster = df_al.rename(columns=kolon_map)[[c for c in kolon_map.values() if c in df_al.rename(columns=kolon_map).columns]]

            def renk_skor(val):
                if isinstance(val, (int,float)):
                    if val >= 78: return "background-color:#1a4a3c;color:#7fffd4"
                    if val >= 65: return "background-color:#1a3a2a;color:#aaffcc"
                    if val >= 50: return "background-color:#3a2e00;color:#ffd700"
                return ""

            def renk_rsi(val):
                if isinstance(val, (int,float)):
                    if 45 <= val <= 65: return "color:#26a69a;font-weight:600"
                    if val > 70:        return "color:#ef5350"
                return ""

            st.dataframe(
                df_goster.style
                    .applymap(renk_skor, subset=["Skor /100"])
                    .applymap(renk_rsi,  subset=["RSI"])
                    .format({
                        "Fiyat ₺": "{:.2f}",    "Skor /100": "{:.1f}",
                        "Teknik /65": "{:.0f}", "Temel /35": "{:.0f}",
                        "RSI": "{:.1f}",         "Hacim Ort.": "{:.2f}",
                        "ATR %": "{:.2f}",       "Boll. Pos %": "{:.1f}",
                        "Momentum 5g %": "{:.2f}","Momentum 20g %": "{:.2f}",
                    }, na_rep="—"),
                use_container_width=True, height=500
            )

            csv = df_al.drop(columns=[c for c in df_al.columns if c.startswith("_")]).to_csv(index=False, encoding="utf-8-sig")
            st.download_button("📥 AL Listesini CSV İndir", csv,
                               f"bist_al_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                               "text/csv")

    # ════════════════════════════
    # TAB 2 — GRAFİKLER
    # ════════════════════════════
    with tab2:
        col_left, col_right = st.columns([1, 2])

        with col_left:
            st.markdown("### Hisse Seç")
            secenek_liste = df_al["ticker"].tolist() if not df_al.empty else df["ticker"].tolist()
            if not secenek_liste:
                st.info("Önce tarama yapın.")
            else:
                secilen = st.selectbox("Hisse", secenek_liste, label_visibility="collapsed")
                secilen_row = df_raw[df_raw["ticker"] == secilen]
                if not secilen_row.empty:
                    row = secilen_row.iloc[0]

                    # Radar grafik
                    st.markdown(f"#### {secilen} — Puan Dağılımı")
                    st.plotly_chart(draw_radar(row), use_container_width=True)

                    # Mini metrik kartları
                    def mini(label, val, good_fn=None):
                        color = "#26a69a" if good_fn and good_fn(val) else "#e0e0e0"
                        st.markdown(f"""
<div style="background:#1a2030;border-radius:8px;padding:8px 12px;margin:4px 0;
            display:flex;justify-content:space-between;align-items:center;">
<span style="color:#888;font-size:12px;">{label}</span>
<span style="color:{color};font-weight:700;font-size:14px;">{val}</span>
</div>""", unsafe_allow_html=True)

                    st.markdown("#### Temel Veriler")
                    mini("F/K",        row["pe"] if row["pe"] else "—",    lambda v: isinstance(v,(int,float)) and v < 15)
                    mini("PD/DD",      row["pb"] if row["pb"] else "—",    lambda v: isinstance(v,(int,float)) and v < 2)
                    mini("Kar Büyüme", f"%{row['earn_g']}" if row["earn_g"] else "—", lambda v: "%" in str(v) and float(str(v).replace("%","")) > 10)
                    mini("Kar Marjı",  f"%{row['profit_m']}" if row["profit_m"] else "—")
                    mini("Sektör",     row["sektor"])

        with col_right:
            if not secenek_liste:
                st.info("Önce tarama yapın.")
            elif not secilen_row.empty:
                st.plotly_chart(draw_chart(row), use_container_width=True)

        # ── Skor Dağılım Grafiği ─────────────────────────────────
        st.markdown("---")
        st.markdown("### 📊 Skor Dağılımı — İlk 40 Hisse")
        if not df.empty:
            top40 = df.head(40)
            fig2 = go.Figure()
            for kolon, renk, isim in [
                ("rsi_p",  "#4A90D9", "RSI"),
                ("macd_p", "#F4A83A", "MACD"),
                ("vol_p",  "#50C878", "Hacim"),
                ("atr_p",  "#E74C3C", "ATR"),
                ("boll_p", "#9B59B6", "Bollinger"),
                ("ma_p",   "#1ABC9C", "MA Bonus"),
                ("pe_p",   "#F39C12", "F/K"),
                ("pb_p",   "#E67E22", "PD/DD"),
                ("eg_p",   "#27AE60", "Kar Büy."),
                ("pm_p",   "#2980B9", "Kar Marjı"),
            ]:
                fig2.add_trace(go.Bar(
                    x=top40["ticker"], y=top40[kolon],
                    name=isim, marker_color=renk
                ))
            fig2.add_hline(y=min_skor, line_dash="dash", line_color="white",
                           annotation_text=f"AL Eşiği ({min_skor})")
            fig2.update_layout(
                barmode="stack", height=430,
                xaxis_tickangle=-50,
                plot_bgcolor="#0f1117", paper_bgcolor="#0f1117", font_color="#e0e0e0",
                legend=dict(orientation="h", y=1.08, font_size=10),
                margin=dict(l=10, r=10, t=30, b=90),
            )
            st.plotly_chart(fig2, use_container_width=True)

        # ── Scatter: RSI vs Skor ──────────────────────────────────
        st.markdown("### 🔵 RSI vs Toplam Skor")
        if not df.empty:
            fig3 = px.scatter(
                df, x="rsi", y="toplam", color="toplam", size="vol_ratio",
                hover_name="ticker", hover_data=["fiyat","pe","pb","macd_lbl"],
                color_continuous_scale="RdYlGn",
                labels={"rsi":"RSI","toplam":"Toplam Skor"},
                height=420
            )
            fig3.add_vline(x=70, line_dash="dash", line_color="#ef5350", line_width=0.8)
            fig3.add_vline(x=30, line_dash="dash", line_color="#26a69a", line_width=0.8)
            fig3.add_hline(y=min_skor, line_dash="dash", line_color="white", line_width=0.8,
                           annotation_text="AL Eşiği")
            fig3.update_layout(
                plot_bgcolor="#0f1117", paper_bgcolor="#0f1117", font_color="#e0e0e0",
                margin=dict(l=10, r=10, t=20, b=10)
            )
            st.plotly_chart(fig3, use_container_width=True)

    # ════════════════════════════
    # TAB 3 — TÜM SONUÇLAR
    # ════════════════════════════
    with tab3:
        st.subheader(f"🗂 Tüm Tarama Sonuçları — Filtresiz ({len(df_raw)} hisse)")

        kolon_map2 = {
            "ticker":"Hisse","sektor":"Sektör","fiyat":"Fiyat ₺",
            "toplam":"Skor /100","teknik_p":"Teknik","temel_p":"Temel",
            "rsi":"RSI","macd_lbl":"MACD","vol_ratio":"Hacim Ort.",
            "atr_pct":"ATR %","mom5":"Momentum 5g %",
            "pe":"F/K","pb":"PD/DD","earn_g":"Kar Büy. %",
        }
        df_raw2 = df_raw.rename(columns=kolon_map2)[[c for c in kolon_map2.values() if c in df_raw.rename(columns=kolon_map2).columns]]
        st.dataframe(df_raw2.style.format(na_rep="—"), use_container_width=True, height=550)

        if show_elim and elenenler:
            st.markdown(f"#### ⛔ Elenen Hisseler ({len(elenenler)} adet — MA Altında)")
            df_el = pd.DataFrame(elenenler)[["ticker","elendi"]]
            df_el.columns = ["Hisse","Sebep"]
            st.dataframe(df_el, use_container_width=True)

        csv2 = df_raw.drop(columns=[c for c in df_raw.columns if c.startswith("_")]).to_csv(index=False, encoding="utf-8-sig")
        st.download_button("📥 Tüm Sonuçları CSV İndir", csv2,
                           f"bist_tum_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                           "text/csv")

    # ════════════════════════════
    # TAB 4 — SİSTEM HAKKINDA
    # ════════════════════════════
    with tab4:
        st.markdown("""
## 📖 Puanlama Sistemi Detayları

### Teknik Analiz — 65 Puan

| Kriter | Max | İdeal Aralık | Açıklama |
|--------|-----|-------------|----------|
| **RSI** | 20 | 42–63 | Momentum güçlü, henüz aşırı alım yok |
| **MACD** | 20 | Histogram büyüyor + MACD > Sinyal | Güçlü momentum sinyali |
| **Hacim** | 12 | 5g/20g > 1.3× | Fiyat hareketi hacimle destekleniyor |
| **ATR Volatilite** | 8 | %1.5–3.5 | Swing için ideal oynaklık aralığı |
| **Bollinger Pos.** | 5 | %20–70 bant içi | Aşırı uçlarda ceza |
| **MA Bonus** | 5 | MA50>MA200, Fiyat MA50'nin %1-12 üstü | Sağlıklı trend yapısı |

> **Zorunlu Filtre:** Fiyat MA50 VE MA200 altındaysa hisse otomatik elenir.

---

### Temel Analiz — 35 Puan

| Kriter | Max | İdeal | Açıklama |
|--------|-----|-------|----------|
| **F/K** | 12 | < 10 | Düşük F/K = ucuz hisse |
| **PD/DD** | 10 | < 1.5 | Defter değerine yakın veya altı |
| **Kar Büyümesi (YoY)** | 8 | > %25 | Çeyreklik kazanç artışı |
| **Net Kar Marjı** | 5 | > %15 | Yüksek marjlı şirket |

> Temel veri alınamayan hisselere nötr puan verilir (elenmiyor).

---

### Skor Yorumlama

| Skor | Yorum |
|------|-------|
| **80–100** | 🟢 Çok Güçlü — Yüksek öncelikli |
| **65–79** | 🟡 Güçlü — AL listesine alınır |
| **50–64** | 🟠 Orta — İzleme listesi |
| **< 50** | ⚪ Zayıf — Geç |

---

### ⚠️ Risk Uyarısı
Bu araç yatırım tavsiyesi vermez. Tüm kararlar yatırımcının kendi sorumluluğundadır.
Geçmiş teknik sinyal başarıları gelecekteki sonuçları garanti etmez.
        """)

    st.success(f"✅ Tarama tamamlandı — {datetime.now().strftime('%d.%m.%Y %H:%M')}")

# ── İlk Açılış Ekranı ────────────────────────────────────────────
else:
    st.markdown("""
<div style="background:#1a2030;border-radius:14px;padding:40px;text-align:center;margin-top:40px;">
<h2 style="color:#4A90D9;">📈 Hoş Geldiniz</h2>
<p style="color:#aaa;font-size:15px;max-width:600px;margin:0 auto;">
Sol panelden hisse sayısı ve filtrelerinizi ayarlayın, ardından<br>
<b style="color:#e0e0e0;">Taramayı Başlat</b> butonuna basın.<br><br>
Sistem seçtiğiniz hisseleri tek tek analiz eder;<br>
teknik ve temel verileri birleştirerek 100 üzerinden puanlar.
</p>
<br>
<div style="display:flex;justify-content:center;gap:30px;flex-wrap:wrap;">
<div style="background:#0f1117;border-radius:10px;padding:16px 24px;border:1px solid #2a3040;">
<div style="font-size:28px;">65</div><div style="color:#888;font-size:12px;">Teknik Puan</div>
</div>
<div style="background:#0f1117;border-radius:10px;padding:16px 24px;border:1px solid #2a3040;">
<div style="font-size:28px;">35</div><div style="color:#888;font-size:12px;">Temel Puan</div>
</div>
<div style="background:#0f1117;border-radius:10px;padding:16px 24px;border:1px solid #2a3040;">
<div style="font-size:28px;">220+</div><div style="color:#888;font-size:12px;">BIST Hissesi</div>
</div>
<div style="background:#0f1117;border-radius:10px;padding:16px 24px;border:1px solid #2a3040;">
<div style="font-size:28px;">10</div><div style="color:#888;font-size:12px;">Kriter</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)
