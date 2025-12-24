# jobs-are-the-way

## Virtual Environment Set-up

For windows, create a VE using:

```powershell
python -m venv .venv
```

and activate by running:

```powershell
venv/scripts/activate
```

Alternatively, if you have installed `make` previously, you can simply run the make command:

```powershell
make virtual-environment
```

## Environmental Variables

Simply copy over the required environmental variables by running:

```powershell
cp .env.example .env
```
