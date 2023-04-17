import pandas as pd
import plotly.express as px
import word_generation as wg


def layout(fig):
    fig.update_layout(
        autosize=False,
        width=1280,
        height=920,
        plot_bgcolor="white",
        legend=dict(
            font=dict(size=10),
            # x=-0,
            # y=-0.4,
            # traceorder="grouped",
            # tracegroupgap=10,
        ),
    )
    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="black",
        gridcolor="grey",
        gridwidth=0.5,
    )
    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor="black",
        gridcolor="grey",
        gridwidth=0.5,
    )
    return fig


def layout2(fig):
    fig.update_layout(
        autosize=False,
        width=1280,
        height=920,
        plot_bgcolor="white",
        legend=dict(
            font=dict(size=10),
            x=-0,
            y=-0.4,
        ),
    )
    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="black",
        gridcolor="grey",
        gridwidth=0.5,
    )
    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor="black",
        gridcolor="grey",
        gridwidth=0.5,
    )
    return fig


def output_generator(fig, name, pee):
    fig.write_image("./courbes_png/" + name + ".png")
    wg.word_generation(
        "./courbes_png/" + name + ".png",
        pee,
        "template.docx",
        "./courbes_word/" + name + ".docx",
        name,
    )


def rcp(ehp_data, pee):
    ehp_data = pd.DataFrame(ehp_data)
    df = ehp_data[["EHP001MP", "EHP002MP"]]
    fig = px.line(
        df,
        title="Evolution de la pression RCP pendant l'EHP",
        labels={
            "index": "Date",
            "value": "Pression (bar)",
            "variable": "Valeurs",
        },
    )
    layout(fig)
    name = "rcp"
    output_generator(fig, name, pee)


def pression_refoulement_mule(ehp_data, app_mode, pee):
    if app_mode == "DPY":
        pression_lim = 236
        pression_arret = 232
        pression_hp = 228
        nom = "RCV191PO"
    if app_mode == "PQY":
        pression_lim = 244
        pression_arret = 239
        pression_hp = 234
        nom = "RCV191PO"
    if app_mode == "900":
        pression_lim = 241
        pression_arret = 235.5
        pression_hp = 230
        nom = "RIS011PO"

    df = ehp_data[["EHP003MP"]]
    df = pd.DataFrame(df)
    df = df.assign(Pression_limite_EHP003MP_236bars=pression_lim)
    df = df.assign(Seuil_d_arrêt_RCV191PO_232bars=pression_arret)
    df = df.assign(
        Seuil_d_alarme_haute_pression_refoulement_RCV191PO_228bars=pression_hp
    )
    fig = px.line(
        df,
        title="Evolution de la pression de refoulement de la pompe " + nom,
        labels={
            "index": "Date",
            "value": "Pression (bar)",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "Pression_limite_EHP003MP_236bars": "Pression limite EHP003MP: "
        + str(pression_lim)
        + "bars",
        "Seuil_d_arrêt_RCV191PO_232bars": "Seuil d'arrêt: "
        + nom
        + " "
        + str(pression_arret)
        + "bars",
        "Seuil_d_alarme_haute_pression_refoulement_RCV191PO_228bars": "Seuil d'alarme haute pression refoulement: "
        + nom
        + " "
        + str(pression_hp)
        + "bars",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))
    layout2(fig)
    name = "pression_refoulement_mule"
    output_generator(fig, name, pee)


def pression_refoulement_mule_detail(ehp_data, app_mode, pee):
    if app_mode == "DPY":
        pression_lim = 236
        pression_arret = 232
        pression_hp = 228
        nom = "RCV191PO"
    if app_mode == "PQY":
        pression_lim = 244
        pression_arret = 239
        pression_hp = 234
        nom = "RCV191PO"
    if app_mode == "900":
        pression_lim = 241
        pression_arret = 235.5
        pression_hp = 230
        nom = "RIS011PO"

    df = ehp_data.loc[ehp_data["EHP003MP"] > 4]
    df = df[["EHP003MP"]]
    df = pd.DataFrame(df)
    df = df.assign(Pression_limite_EHP003MP_236bars=pression_lim)
    df = df.assign(Seuil_d_arrêt_RCV191PO_232bars=pression_arret)
    df = df.assign(
        Seuil_d_alarme_haute_pression_refoulement_RCV191PO_228bars=pression_hp
    )
    fig = px.line(
        df,
        title="Evolution de la pression de refoulement de la pompe "
        + nom
        + " pendant l'épreuve",
        labels={
            "index": "Date",
            "value": "Pression (bar)",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "Pression_limite_EHP003MP_236bars": "Pression limite EHP003MP: "
        + str(pression_lim)
        + "bars",
        "Seuil_d_arrêt_RCV191PO_232bars": "Seuil d'arrêt: "
        + nom
        + " "
        + str(pression_arret)
        + "bars",
        "Seuil_d_alarme_haute_pression_refoulement_RCV191PO_228bars": "Seuil d'alarme haute pression refoulement: "
        + nom
        + " "
        + str(pression_hp)
        + "bars",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))
    layout2(fig)
    name = "pression_refoulement_mule_detail"
    output_generator(fig, name, pee)


def temperature_gros_composants_fond_de_cuve(ehp_data, pee):
    df = ehp_data[["EHP001MT", "EHP002MT", "EHP003MT", "EHP011MT"]]
    fig = px.line(
        df,
        title="Evolution de la temperature des gros composants - Fond de cuve",
        labels={
            "index": "Date",
            "value": "Température °C",
            "variable": "Valeurs",
        },
    )
    layout(fig)
    name = "temperature_gros_composants_fond_de_cuve"
    output_generator(fig, name, pee)


def temperature_gros_composants_couvercle_et_pressu(ehp_data, pee):
    df = ehp_data[
        [
            "EHP004MT",
            "EHP005MT",
            "EHP006MT",
            "EHP012MT",
            "EHP013MT",
            "EHP014MT",
        ]
    ]
    fig = px.line(
        df,
        title="Evolution de la temperature des gros composants ",
        labels={
            "index": "Date",
            "value": "Température °C",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "EHP004MT": "EHP004MT - Bride de cuve",
        "EHP005MT": "EHP005MT - Bride de couvercle",
        "EHP006MT": "EHP006MT - JEP Pressu",
        "EHP012MT": "EHP012MT - Bride de cuve",
        "EHP013MT": "EHP013MT - Bride de couvercle",
        "EHP014MT": "EHP014MT - JEP Pressu",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))
    layout(fig)
    name = "temperature_gros_composants_brides_JEP"
    output_generator(fig, name, pee)


def temperature_gros_composants_gv(ehp_data, app_mode, pee):
    if app_mode == "900":
        df = ehp_data[
            [
                "EHP007MT",
                "EHP008MT",
                "EHP009MT",
                "EHP015MT",
                "EHP016MT",
                "EHP017MT",
            ]
        ]
        fig = px.line(
            df,
            title="Evolution de la temperature des gros composants - GVs",
            labels={
                "index": "Date",
                "value": "Température (°C)",
                "variable": "Valeurs",
            },
        )
        value_map = {
            "EHP007MT": "EHP007MT - GV1",
            "EHP008MT": "EHP008MT - GV2",
            "EHP009MT": "EHP009MT - GV3",
            "EHP015MT": "EHP015MT - GV1",
            "EHP016MT": "EHP016MT - GV2",
            "EHP017MT": "EHP017MT - GV3",
        }
        fig.for_each_trace(
            lambda t: t.update(
                name=value_map.get(
                    t.name,
                    t.name,
                )
            )
        )

    if app_mode == "PQY" or app_mode == "DPY":
        df = ehp_data[
            [
                "EHP007MT",
                "EHP008MT",
                "EHP009MT",
                "EHP010MT",
                "EHP015MT",
                "EHP016MT",
                "EHP017MT",
                "EHP018MT",
            ]
        ]
        fig = px.line(
            df,
            title="Evolution de la temperature des gros composants - GV",
            labels={
                "index": "Date",
                "value": "Température (°C)",
                "variable": "Valeurs",
            },
        )
        value_map = {
            "EHP007MT": "EHP007MT - GV1",
            "EHP008MT": "EHP008MT - GV2",
            "EHP009MT": "EHP009MT - GV3",
            "EHP010MT": "EHP010MT - GV4",
            "EHP015MT": "EHP015MT - GV1",
            "EHP016MT": "EHP016MT - GV2",
            "EHP017MT": "EHP017MT - GV3",
            "EHP018MT": "EHP018MT - GV4",
        }
        fig.for_each_trace(
            lambda t: t.update(
                name=value_map.get(
                    t.name,
                    t.name,
                )
            )
        )
    layout(fig)
    name = "temperature_gros_composants_gv"
    output_generator(fig, name, pee)


def pgrad(ehp_data, pee):
    df = ehp_data[["EHP001MPGrad", "EHP002MPGrad"]]
    df = df.assign(val_max_grad=4)
    df = df.assign(val_min_grad=-4)
    fig = px.line(
        df,
        title="Gradients de Pression de l'EHP",
        labels={
            "index": "Date",
            "value": "Gradient de Pression (bar/min)",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "val_max_grad": "Valeur Max Gradient (+4 bar/min)",
        "val_min_grad": "Valeur Min Gradient (-4 bar/min)",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))
    layout(fig)
    name = "gradients_de_pression"
    output_generator(fig, name, pee)


def tmoy(ehp_data, pee):
    df = ehp_data[["TMOY"]]
    fig = px.line(
        df,
        title="Suivi de la Tmoy de l'EHP",
        labels={
            "index": "Date",
            "value": "Température (°C)",
            "variable": "Valeurs",
        },
    )
    layout(fig)
    name = "Tmoy"
    output_generator(fig, name, pee)


def tgrad(ehp_data, pee, seg):
    TmoySup = 28
    TmoyInf = -28

    df = ehp_data[["TMOY", "TGRAD"]]
    df = df.assign(Tmoymin=-14)
    df = df.assign(Tmoymax=14)
    df.loc[df.TMOY > seg, "Tmoymax"] = TmoySup
    df.loc[df.TMOY > seg, "Tmoymin"] = TmoyInf
    df = df[["TGRAD", "Tmoymax", "Tmoymin"]]

    fig = px.line(
        df,
        title="Suivi du gradient de Tmoy de l'EHP",
        labels={
            "index": "Date",
            "value": "Température (°C/h)",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "Tmoymin": "Tmoymin -14°C/h & -28°C/h",
        "Tmoymax": "Tmoymax +14°C/h & +28°C/h",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))
    layout(fig)
    name = "Tgrad"
    output_generator(fig, name, pee)


def tfluid1(ehp_data, app_mode, pee):
    df = ehp_data[["RCP009MT", "RCP010MT", "RCP028MT"]]
    fig = px.line(
        df,
        title="Suivi des températures fluide pendant l'EHP",
        labels={
            "index": "Date",
            "value": "Température (°C)",
            "variable": "Valeurs",
        },
    )
    if app_mode == "PQY" or app_mode == "DPY":
        value_map = {
            "RCP009MT": "RCP009MT",
            "RCP010MT": "RCP014MT",
            "RCP028MT": "RCP100MT",
        }
        fig.for_each_trace(
            lambda t: t.update(
                name=value_map.get(
                    t.name,
                    t.name,
                )
            )
        )
    layout(fig)
    name = "Tfluide1"
    output_generator(fig, name, pee)


def tfluid2(ehp_data, app_mode, pee):
    df = ehp_data[["RCP029MT", "RCP043MT", "RCP044MT"]]
    fig = px.line(
        df,
        title="Suivi des températures fluide pendant l'EHP",
        labels={
            "index": "Date",
            "value": "Température (°C)",
            "variable": "Valeurs",
        },
    )
    if app_mode == "PQY" or app_mode == "DPY":
        value_map = {
            "RCP029MT": "RCP104MT",
            "RCP043MT": "RCP200MT",
            "RCP044MT": "RCP204MT",
        }
        fig.for_each_trace(
            lambda t: t.update(
                name=value_map.get(
                    t.name,
                    t.name,
                )
            )
        )
    layout(fig)
    name = "Tfluide2"
    output_generator(fig, name, pee)


def tfluid3(ehp_data, app_mode, pee):
    if app_mode == "PQY" or app_mode == "DPY":
        df = ehp_data[["RCP055MT", "RCP056MT", "RCP400MT", "RCP404MT"]]
    if app_mode == "900":
        df = ehp_data[["RCP055MT", "RCP056MT"]]
    fig = px.line(
        df,
        title="Suivi des températures fluide pendant l'EHP",
        labels={
            "index": "Date",
            "value": "Température (°C)",
            "variable": "Valeurs",
        },
    )
    if app_mode == "PQY" or app_mode == "DPY":
        value_map = {
            "RCP055MT": "RCP104MT",
            "RCP056MT": "RCP200MT",
            "RCP400MT": "RCP204MT",
            "RCP404MT": "RCP404MT",
        }
        fig.for_each_trace(
            lambda t: t.update(
                name=value_map.get(
                    t.name,
                    t.name,
                )
            )
        )
    layout(fig)
    name = "Tfluide3"
    output_generator(fig, name, pee)


def tmetal1(ehp_data, pee):
    df = ehp_data[["EHP001MT_EHP002MTGrad", "EHP011MT_EHP003MTGrad"]]
    fig = px.line(
        df,
        title="Gradient des températures métal pendant l'EHP - Fond de cuve",
        labels={
            "index": "Date",
            "value": "Température (°C/h)",
            "variable": "Valeurs",
        },
    )
    layout(fig)
    name = "Tmetal1"
    output_generator(fig, name, pee)


def tmetal2(ehp_data, pee):
    df = ehp_data[
        [
            "EHP004MT_EHP012MTGrad",
            "EHP013MT_EHP005MTGrad",
            "EHP006MT_EHP014MTGrad",
        ]
    ]
    fig = px.line(
        df,
        title="Gradient des températures métal pendant l'EHP - Couvercle et Pressu",
        labels={
            "index": "Date",
            "value": "Température (°C/h)",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "EHP004MT_EHP012MTGrad": "Max EHP004MTGrad/EHP012MTGrad - Bride de cuve",
        "EHP013MT_EHP005MTGrad": "Max EHP005MTGrad/EHP013MTGrad - Bride de couvercle",
        "EHP006MT_EHP014MTGrad": "Max EHP006MTGrad/EHP014MTGrad - JEP Pressu",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))
    layout(fig)
    name = "Tmetal2"
    output_generator(fig, name, pee)


def tmetal3(ehp_data, app_mode, pee):
    if app_mode == "PQY" or app_mode == "DPY":
        df = ehp_data[
            [
                "EHP007MT_EHP015MTGrad",
                "EHP008MT_EHP016MTGrad",
                "EHP017MT_EHP009MTGrad",
                "EHP018MT_EHP010MTGrad",
            ]
        ]
    if app_mode == "900":
        df = ehp_data[
            [
                "EHP007MT_EHP015MTGrad",
                "EHP008MT_EHP016MTGrad",
                "EHP017MT_EHP009MTGrad",
            ]
        ]
    fig = px.line(
        df,
        title="Gradient des températures métal pendant l'EHP - GV",
        labels={
            "index": "Date",
            "value": "Température (°C/h)",
            "variable": "Valeurs",
        },
    )
    if app_mode == "PQY" or app_mode == "DPY":
        value_map = {
            "EHP007MT_EHP015MTGrad": "Max EHP007MTGrad/EHP015MTGrad - GV1",
            "EHP008MT_EHP016MTGrad": "Max EHP008MTGrad/EHP016MTGrad - GV2",
            "EHP017MT_EHP009MTGrad": "Max EHP009MTGrad/EHP017MTGrad - GV3",
            "EHP018MT_EHP010MTGrad": "Max EHP010MTGrad/EHP018MTGrad - GV4",
        }
    if app_mode == "900":
        value_map = {
            "EHP007MT_EHP015MTGrad": "Max EHP007MTGrad/EHP015MTGrad - GV1",
            "EHP008MT_EHP016MTGrad": "Max EHP008MTGrad/EHP016MTGrad - GV2",
            "EHP017MT_EHP009MTGrad": "Max EHP009MTGrad/EHP017MTGrad - GV3",
        }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))
    layout(fig)
    name = "Tmetal3"
    output_generator(fig, name, pee)


def evolution_pression_epreuve(ehp_data, pee):
    df = ehp_data.loc[ehp_data["EHP001MP"] > 172]
    df = df[["EHP001MP"]]
    df2 = ehp_data.loc[ehp_data["EHP002MP"] > 172]
    df2 = df2[["EHP002MP"]]
    df = pd.concat([df, df2])
    df = df.sort_values(by="index")
    df = df.interpolate()
    df = df.assign(pression_max=207.8)
    df = df.assign(pression_min=206.9)
    fig = px.line(
        df,
        title="Evolution de la pression primaire pendant l'épreuve",
        labels={
            "index": "Date",
            "value": "Pression (bar)",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "pression_max": "207,8 bar",
        "pression_min": "206,9 bar",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))
    layout(fig)
    name = "P_primaire_epreuve"
    output_generator(fig, name, pee)


def evolution_pression_epreuve_palier(ehp_data, pee):
    df = ehp_data.loc[ehp_data["EHP001MP"] > 205]
    df = df[["EHP001MP"]]
    df2 = ehp_data.loc[ehp_data["EHP002MP"] > 205]
    df2 = df2[["EHP002MP"]]
    df = pd.concat([df, df2])
    df = df.sort_values(by="index")
    df = df.interpolate()
    df = df.assign(pression_max=206.9)
    df = df.assign(pression_min=206)
    fig = px.line(
        df,
        title="Evolution de la pression primaire pendant le palier d'épreuve",
        labels={
            "index": "Date",
            "value": "Pression (bar)",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "pression_max": "206,9 bar",
        "pression_min": "206 bar",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))
    layout(fig)
    name = "P_primaire_palier"
    output_generator(fig, name, pee)


def hors_criteres(ehp_data, seg):
    ## EHP001MP
    df = ehp_data
    df = df.loc[df["EHP001MPGrad"] < -4]
    df = df[["EHP001MPGrad"]]
    df.to_excel("Hors_critères/EHP1MPGrad_inf-4.xlsx")

    df = ehp_data
    df = df.loc[df["EHP001MPGrad"] > 4]
    df = df[["EHP001MPGrad"]]
    df.to_excel("Hors_critères/EHP1MPGrad_sup4.xlsx")

    ## EHP002MP
    df = ehp_data
    df = df.loc[df["EHP002MPGrad"] < -4]
    df = df[["EHP002MPGrad"]]
    df.to_excel("Hors_critères/EHP2MPGrad_inf-4.xlsx")

    df = ehp_data
    df = df.loc[df["EHP002MPGrad"] > 4]
    df = df[["EHP002MPGrad"]]
    df.to_excel("Hors_critères/EHP2MPGrad_sup4.xlsx")

    ##TGRAD
    df = ehp_data.loc[ehp_data["TMOY"] > seg]
    df2 = df.loc[df["TGRAD"] < -28]
    df2 = df2[["TGRAD"]]
    df2.to_excel("Hors_critères/TGRAD_inf-28.xlsx")

    df2 = df.loc[df["TGRAD"] > 28]
    df2 = df2[["TGRAD"]]
    df2.to_excel("Hors_critères/TGRAD_sup28.xlsx")

    df = ehp_data.loc[ehp_data["TMOY"] < seg]
    df2 = df.loc[df["TGRAD"] < -14]
    df2 = df2[["TGRAD"]]
    df2.to_excel("Hors_critères/TGRAD_inf-14.xlsx")

    df2 = df.loc[df["TGRAD"] > 14]
    df2 = df2[["TGRAD"]]
    df2.to_excel("Hors_critères/TGRAD_sup14.xlsx")
