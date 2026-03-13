FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore dependencies
COPY *.csproj .
RUN dotnet restore

# Copy everything else and build
COPY . .
RUN dotnet publish -c Release -o /app/publish

# Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
EXPOSE 5000

# Copy published app
COPY --from=build /app/publish .

# Set environment variable for ASP.NET Core URLs
ENV ASPNETCORE_URLS=http://+:5000

ENTRYPOINT ["dotnet", "YourProject.dll"]