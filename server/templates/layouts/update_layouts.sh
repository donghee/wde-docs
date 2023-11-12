(cd ~/src/wde-docs; npx tailwindcss -i ./server/input.css -o ./server/static/output.css)

mkdir ~/src/wde-usability/web/static/
mkdir ~/src/wde-wearability/web/static/
mkdir ~/src/wde-interactivity/web/static/
mkdir ~/src/wde-visualization/web/static/

cp ~/src/wde-docs/server/static/output.css ~/src/wde-usability/web/static/
cp ~/src/wde-docs/server/static/output.css ~/src/wde-wearability/web/static/
cp ~/src/wde-docs/server/static/output.css ~/src/wde-interactivity/web/static/
cp ~/src/wde-docs/server/static/output.css ~/src/wde-visualization/web/static/

cp *.html ~/src/wde-usability/web/templates/layouts/
cp *.html ~/src/wde-wearability/web/templates/layouts/
cp *.html ~/src/wde-interactivity/web/templates/layouts/
cp *.html ~/src/wde-visualization/web/templates/layouts/
