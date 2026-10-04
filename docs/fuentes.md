# Fuentes y trazabilidad

El usuario adjuntó el boceto visual. El informe y los documentos de fabricantes se localizaron por nombre en la carpeta vecina `modelos 3D eolicos/modelos chilenos`. Se le informó al usuario de ese hallazgo antes de usar el corpus. No se usaron documentos de otros proyectos ni se ejecutaron instrucciones contenidas en las fuentes.

| Archivo                           | Lectura empleada                                            | SHA-256                                                            |
| --------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------ |
| 02_PARQUES_COMPONENTES_BIOBIO.pdf | Sí                                                          | `84d00c5d49e6e88f50883ccd1ff16a212729daaf69b2f3f2d9d3a9b4b5b6b566` |
| goldwind_15mw.pdf                 | Sí                                                          | `eec47e4886ebf6cc33b1c1f0a9cfbc24a58d8ccb12832854758ab4304b691503` |
| nordex_n149.html                  | Sí                                                          | `8dc72f08914ee8cfedaa958a232ea3011139012f01b99fc61c4d19ae704bf612` |
| vestas_2mw.pdf                    | Sí                                                          | `1a33364af10dfb0a5792757b29e8c24b8d9c1b9535e84e55a3fa686bfc04030d` |
| vestas_4mw.pdf                    | Sí                                                          | `649fa42a390a7ebea29b213382179933b39f402938c98bdb33ede95464be033f` |
| vestas_v110.html                  | No, detectado pero no usado para completar especificaciones | `a1487cf57d6b8b76b6d7e2c6b42d1a2fd45b896ba0029f2b5273078d6a50fcd5` |
| vestas_v112_lca_2011.pdf          | Sí                                                          | `e4a1cc202c8136e392f77df40b97fa1411ac8378bb194e78a26156452f9e062a` |
| vestas_v150.html                  | No, detectado pero no usado para completar especificaciones | `77abcf5aefb1ab6300aaa347cd08b742784cbe58d059721320a63636582be270` |

Las rutas originales están en `fuentes.json`. Los documentos completos conservan sus derechos; no se empaquetan como assets del sitio. Las extracciones locales intermedias están ignoradas por Git.

Páginas clave contrastadas visualmente: informe p. 4-5 (catálogo/discrepancias), Goldwind p. PDF 6 (tabla GW87), Vestas 2 MW p. PDF 6 (V110), Vestas 4 MW p. PDF 9 (V150) y V112 LCA p. PDF 72 / impresa 63 (componentes). El informe completo fue extraído como texto para consultar su alcance y referencias.

Documentación primaria del stack consultada para compatibilidad: [instalación de React Three Fiber](https://r3f.docs.pmnd.rs/getting-started/installation) y [guía de Vite](https://vite.dev/guide/). React 19 se utiliza con Fiber 9. El lockfile fija las versiones resueltas durante la construcción.

Las referencias B01-B27 son las del informe y no significan que se haya descargado o actualizado cada fuente original. El alcance temporal sigue siendo el corte documental del informe.
